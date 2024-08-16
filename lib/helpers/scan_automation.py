import logging
import time
from .insightappsec import InsightAppSec


def create_scan(api_key: str, region: str, settings: dict):
    try:
        url = f"https://{region}.api.insight.rapid7.com/ias/v1"
        api = InsightAppSec(url=url, api_key=api_key)

        # Step 1 - Read values from config file
        scan_pairs_names, interval = read_settings(settings)

        # Step 2 - Grab IDs for application names and scan config names
        scan_pairs_ids = get_ids(api, scan_pairs_names)
        
        # Step 3 - Submit all scans
        scan_ids = submit_scans(api, scan_pairs_ids)
        id_to_names = {} # scan ID - > (app name, scan config name)
        for i in range(0, len(scan_ids)):
            scan_id = scan_ids[i]
            id_to_names[scan_id] = scan_pairs_names[i]

        # Step 4 - Track scan status
        track_scans(api, scan_ids, id_to_names, interval)

        # Step 5 - Report Findings
        report_findings(api, scan_ids, id_to_names)

    except Exception as e:
        logging.error(f"Encountered error while creating scans: {e}")

def report_findings(api: InsightAppSec, scan_ids: [str], id_to_names: dict):
    """
    Given list of scan IDs, report on number of vulnerabilities found and their details.
    """
    logging.info("REPORTING VULNERABILITY DETAILS OF SCANS... (Scan ID, App Name, Scan Config Name): NUM VULNS")
    for scan_id in scan_ids:
        try:
            details = api.get_vulnerabilities(scan_id)
            num_findings = len(details)

            logging.info(f"({scan_id}, {id_to_names.get(scan_id)[0]}, {id_to_names.get(scan_id)[1]}): {num_findings} vulnerabilities found")

            # Log each vulnerability found
            for vuln in details:
                severity = vuln.get("severity")
                vuln_name = vuln.get("name", "Unknown Vulnerability")
                vuln_description = vuln.get("description", "No description available")
                logging.info(f"Vulnerability found - Name: {vuln_name}, Severity: {severity}, Description: {vuln_description}, Scan ID: {scan_id}")
                if severity == "HIGH":
                    logging.warning(f"High severity vulnerability found! Immediate attention required. Scan ID: {scan_id}, App Name: {id_to_names.get(scan_id)[0]}, Scan Config Name: {id_to_names.get(scan_id)[1]}")
                elif severity == "LOW":
                    logging.info(f"Low severity vulnerability found. Please review. Scan ID: {scan_id}, App Name: {id_to_names.get(scan_id)[0]}, Scan Config Name: {id_to_names.get(scan_id)[1]}")
        except Exception as e:
            logging.error(f"Error reporting findings for scan ID {scan_id}: {e}")





def track_scans(api: InsightAppSec, scan_ids: [str], id_to_names: dict, interval: int):
    """
    Tracks the status of all current scans being run
    """
    scan_ids_copy = list(scan_ids)
    stop_criteria = ["COMPLETE", "FAILED"]
    start = time.time()
    logging.info("CHECKING STATUS OF REMAINING SCANS... (Scan ID, App Name, Scan Config Name): STATUS")
    for scan_id in scan_ids_copy:
        log_status(api, scan_id, id_to_names)
    while len(scan_ids_copy):
        if time.time() - start > interval:
            logging.info("CHECKING STATUS OF REMAINING SCANS... (Scan ID, App Name, Scan Config Name): STATUS")
            to_remove = []
            for scan_id in scan_ids_copy:
                scan_status = log_status(api, scan_id, id_to_names)
                if scan_status in stop_criteria:
                    to_remove.append(scan_id)
            for scan_id in to_remove: # remove scans that completed or failed
                scan_ids_copy.remove(scan_id)
            start = time.time()

def read_settings(settings: dict):
    """
    Takes in settings dictionary and returns list of tuples (app name, scan config name)
    """
    scan_pairs = [] # list of tuples (app name, scan config name)
    for scan in settings.get("scan_info"):
        app_name = scan.get("app_name")
        scan_config_name = scan.get("scan_config_name")
        if app_name is None or scan_config_name is None:
            logging.error("Application name and scan config must be set up in configuration file")
            return
        scan_pairs.append((app_name, scan_config_name))

    interval = settings.get("status_check_interval", 60)
    return scan_pairs, interval

def submit_scans(api: InsightAppSec, scan_pairs: [(str, str)]):
    """
    Takes in instance of authenticated IAS API object and list of tuples of scan info (using IDs).
    Triggers all of the scans and returns a list of scan IDs
    """
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
    """
    Takes in instance of authenticated IAS API object and list of tuples of scan info (using names).
    Returns list of tuples of scan info with names converted to IDs
    """
    scan_pairs_ids = []
    for scan_pair in scan_pairs:
        app_results = api.search("APP", f"app.name='{scan_pair[0]}'")
        if app_results is None or app_results == []:
            logging.info(f"Application with name '{scan_pair[0]}' could not be found - skipping scan")
            continue
        else:
            app_id = app_results[0].get("id")
            

        scan_config_results = api.search("SCAN_CONFIG", f"scanconfig.name='{scan_pair[1]}'&&scanconfig.app.id='{app_id}'")
        if scan_config_results is None or scan_config_results == []:
            logging.error(f"Scan config with name '{scan_pair[1]}' could not be found in {app_id} - skipping scan")
            continue
        else:
            scan_config_id = scan_config_results[0].get("id")
        scan_pairs_ids.append((app_id, scan_config_id))
    return scan_pairs_ids

def log_status(api: InsightAppSec, scan_id: str, id_to_names: dict) -> str:
    """
    Logs current status of a scan given its ID
    """
    scan = api.get_scan(scan_id)
    scan_status = scan.get("status")
    logging.info(f"({scan_id}, {id_to_names.get(scan_id)[0]}, {id_to_names.get(scan_id)[1]}): {scan_status}")
    if scan_status == "FAILED":
        failure_reason = scan.get("failure_reason")
        logging.info(f"Reason for failure: {failure_reason}")
    return scan_status






# import logging
# import time
# from .insightappsec import InsightAppSec


# def create_scan(api_key: str, region: str, settings: dict):
#     try:
#         url = f"https://{region}.api.insight.rapid7.com/ias/v1"
#         api = InsightAppSec(url=url, api_key=api_key)

#         # Step 1 - Read values from config file
#         scan_pairs_names, interval = read_settings(settings)

#         # Step 2 - Grab IDs for application names and scan config names
#         scan_pairs_ids = get_ids(api, scan_pairs_names)
        
#         # Step 3 - Submit all scans
#         scan_ids = submit_scans(api, scan_pairs_ids)
#         id_to_names = {} # scan ID - > (app name, scan config name)
#         for i in range(0, len(scan_ids)):
#             scan_id = scan_ids[i]
#             id_to_names[scan_id] = scan_pairs_names[i]

#         # Step 4 - Track scan status
#         track_scans(api, scan_ids, id_to_names, interval)

#         # Step 5 - Report Findings
#         report_findings(api, scan_ids, id_to_names)

#     except Exception as e:
#         logging.error(f"Encountered error while creating scans: {e}")

# def report_findings(api: InsightAppSec, scan_ids: [str], id_to_names: dict):
#     """
#     Given list of scan IDs, report on number of vulnerabilities found
#     """
#     logging.info("REPORTING VULNERABILITY COUNTS OF SCANS... (Scan ID, App Name, Scan Config Name): NUM VULNS")
#     for scan_id in scan_ids:
#         try:
#             details = api.search('VULNERABILITY', f"vulnerability.scans.id='{scan_id}'")
#             if details is None:
#                 logging.warning(f"No details returned for scan ID {scan_id}")
#                 continue

#             if isinstance(details, list) and len(details) > 0:
#                 num_findings = details[0].get("metadata", {}).get("total_data", 0)
#                 vulns = details[0].get("data", [])
#             elif isinstance(details, dict):
#                 num_findings = details.get("metadata", {}).get("total_data", 0)
#                 vulns = details.get("data", [])
#             else:
#                 logging.error(f"Unexpected response format for scan ID {scan_id}: {details}")
#                 num_findings = 0
#                 vulns = []

#             logging.info(f"({scan_id}, {id_to_names.get(scan_id)[0]}, {id_to_names.get(scan_id)[1]}): {num_findings}")

#             # Check vulnerabilities severity
#             for vuln in vulns:
#                 severity = vuln.get("severity")
#                 if severity == "HIGH":
#                     logging.warning(f"High severity vulnerability found! Immediate attention required. Scan ID: {scan_id}, App Name: {id_to_names.get(scan_id)[0]}, Scan Config Name: {id_to_names.get(scan_id)[1]}")
#                 elif severity == "LOW":
#                     logging.info(f"Low severity vulnerability found. Please review. Scan ID: {scan_id}, App Name: {id_to_names.get(scan_id)[0]}, Scan Config Name: {id_to_names.get(scan_id)[1]}")
#         except Exception as e:
#             logging.error(f"Error reporting findings for scan ID {scan_id}: {e}")




# def track_scans(api: InsightAppSec, scan_ids: [str], id_to_names: dict, interval: int):
#     """
#     Tracks the status of all current scans being run
#     """
#     scan_ids_copy = list(scan_ids)
#     stop_criteria = ["COMPLETE", "FAILED"]
#     start = time.time()
#     logging.info("CHECKING STATUS OF REMAINING SCANS... (Scan ID, App Name, Scan Config Name): STATUS")
#     for scan_id in scan_ids_copy:
#         log_status(api, scan_id, id_to_names)
#     while len(scan_ids_copy):
#         if time.time() - start > interval:
#             logging.info("CHECKING STATUS OF REMAINING SCANS... (Scan ID, App Name, Scan Config Name): STATUS")
#             to_remove = []
#             for scan_id in scan_ids_copy:
#                 scan_status = log_status(api, scan_id, id_to_names)
#                 if scan_status in stop_criteria:
#                     to_remove.append(scan_id)
#             for scan_id in to_remove: # remove scans that completed or failed
#                 scan_ids_copy.remove(scan_id)
#             start = time.time()

# def read_settings(settings: dict):
#     """
#     Takes in settings dictionary and returns list of tuples (app name, scan config name)
#     """
#     scan_pairs = [] # list of tuples (app name, scan config name)
#     for scan in settings.get("scan_info"):
#         app_name = scan.get("app_name")
#         scan_config_name = scan.get("scan_config_name")
#         if app_name is None or scan_config_name is None:
#             logging.error("Application name and scan config must be set up in configuration file")
#             return
#         scan_pairs.append((app_name, scan_config_name))

#     interval = settings.get("status_check_interval", 60)
#     return scan_pairs, interval

# def submit_scans(api: InsightAppSec, scan_pairs: [(str, str)]):
#     """
#     Takes in instance of authenticated IAS API object and list of tuples of scan info (using IDs).
#     Triggers all of the scans and returns a list of scan IDs
#     """
#     scan_ids = []
#     for scan_pair in scan_pairs:
#         body = {
#             "app": {
#                 "id": scan_pair[0]
#             },
#             "scan_config": {
#                 "id": scan_pair[1]
#             }
#         }
#         scan_id = api.submit_scan(body)
#         scan_ids.append(scan_id)
#     return scan_ids

# def get_ids(api: InsightAppSec, scan_pairs: [(str, str)]):
#     """
#     Takes in instance of authenticated IAS API object and list of tuples of scan info (using names).
#     Returns list of tuples of scan info with names converted to IDs
#     """
#     scan_pairs_ids = []
#     for scan_pair in scan_pairs:
#         app_results = api.search("APP", f"app.name='{scan_pair[0]}'")
#         if app_results is None or app_results == []:
#             logging.info(f"Application with name '{scan_pair[0]}' could not be found - skipping scan")
#             continue
#         else:
#             app_id = app_results[0].get("id")
            

#         scan_config_results = api.search("SCAN_CONFIG", f"scanconfig.name='{scan_pair[1]}'&&scanconfig.app.id='{app_id}'")
#         if scan_config_results is None or scan_config_results == []:
#             logging.error(f"Scan config with name '{scan_pair[1]}' could not be found in {app_id} - skipping scan")
#             continue
#         else:
#             scan_config_id = scan_config_results[0].get("id")
#         scan_pairs_ids.append((app_id, scan_config_id))
#     return scan_pairs_ids

# def log_status(api: InsightAppSec, scan_id: str, id_to_names: dict) -> str:
#     """
#     Logs current status of a scan given its ID
#     """
#     scan = api.get_scan(scan_id)
#     scan_status = scan.get("status")
#     logging.info(f"({scan_id}, {id_to_names.get(scan_id)[0]}, {id_to_names.get(scan_id)[1]}): {scan_status}")
#     if scan_status == "FAILED":
#         failure_reason = scan.get("failure_reason")
#         logging.info(f"Reason for failure: {failure_reason}")
#     return scan_status
