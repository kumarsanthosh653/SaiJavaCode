import time
from .insightappsec import InsightAppSec


def create_scan(api_key: str, region: str, settings: dict):
    try:
        url = f"https://{region}.api.insight.rapid7.com/ias/v1"
        api = InsightAppSec(url=url, api_key=api_key)

        scan_pairs_names, interval = read_settings(settings)
        scan_pairs_ids = get_ids(api, scan_pairs_names)
        scan_ids = submit_scans(api, scan_pairs_ids)

        id_to_names = {scan_ids[i]: scan_pairs_names[i] for i in range(len(scan_ids))}
        track_scans(api, scan_ids, id_to_names, interval)
        report_findings(api, scan_ids, id_to_names)

    except Exception as e:
        print(f"Encountered error while creating scans: {e}")

def report_findings(api: InsightAppSec, scan_ids: [str], id_to_names: dict):
    print("REPORTING VULNERABILITY DETAILS OF SCANS... (Scan ID, App Name, Scan Config Name): DETAILS")
    for scan_id in scan_ids:
        vulnerabilities = api.get_vulnerabilities(scan_id)
        num_findings = len(vulnerabilities.get("data", []))
        print(f"({scan_id}, {id_to_names.get(scan_id)[0]}, {id_to_names.get(scan_id)[1]}: {num_findings} vulnerabilities found)")

        for vuln in vulnerabilities.get("data", []):
            vuln_id = vuln.get("id")
            severity = vuln.get("severity")
            description = vuln.get("description")
            print(f"Vuln ID: {vuln_id}, Severity: {severity}, Description: {description}")

def track_scans(api: InsightAppSec, scan_ids: [str], id_to_names: dict, interval: int):
    stop_criteria = ["COMPLETE", "FAILED"]
    print("CHECKING STATUS OF REMAINING SCANS... (Scan ID, App Name, Scan Config Name): STATUS")
    while len(scan_ids):
        time.sleep(interval)
        to_remove = []
        for scan_id in scan_ids:
            scan_status = log_status(api, scan_id, id_to_names)
            if scan_status in stop_criteria:
                to_remove.append(scan_id)
        for scan_id in to_remove:
            scan_ids.remove(scan_id)

def read_settings(settings: dict):
    scan_pairs = [(scan.get("app_name"), scan.get("scan_config_name")) for scan in settings.get("scan_info")]
    interval = settings.get("status_check_interval", 60)
    return scan_pairs, interval

def submit_scans(api: InsightAppSec, scan_pairs: [(str, str)]):
    scan_ids = []
    for scan_pair in scan_pairs:
        body = {
            "app": {
                "id": scan_pair[0]
            },
            "scan_config": {
                "id": scan_pair[1]
            }
        }
        scan_id = api.submit_scan(body)
        scan_ids.append(scan_id)
    return scan_ids

def get_ids(api: InsightAppSec, scan_pairs: [(str, str)]):
    scan_pairs_ids = []
    for scan_pair in scan_pairs:
        app_name, scan_config_name = scan_pair
        apps = api.search("APPLICATION", f"app.name = '{app_name}'")
        app_id = apps[0].get("id")
        scan_configs = api.search("SCAN_CONFIG", f"scan_config.name = '{scan_config_name}'")
        scan_config_id = scan_configs[0].get("id")
        scan_pairs_ids.append((app_id, scan_config_id))
    return scan_pairs_ids

def log_status(api: InsightAppSec, scan_id: str, id_to_names: dict):
    scan = api.get_scan(scan_id)
    status = scan.get("status")
    print(f"({scan_id}, {id_to_names.get(scan_id)[0]}, {id_to_names.get(scan_id)[1]}): {status}")
    if status == "FAILED":
        print(f"Reason for failure: {scan.get('failure_reason')}")
    return status
