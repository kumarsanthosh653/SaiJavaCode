import requests

# Replace with your InsightAppSec API key
API_KEY = "f8096810-123c-43c9-87c8-cc76cebea7ec"

# Base URL for InsightAppSec API
BASE_URL = "https://us.api.insight.rapid7.com/ias/v1"

# Headers for authentication
HEADERS = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

def get_scan_vulnerabilities(scan_id):
    """
    Retrieve vulnerabilities specific to a given scan ID.
    """
    vulnerabilities_endpoint = f"{BASE_URL}/vulnerabilities"
    params = {
        "filter[scan.id]": scan_id
    }

    response = requests.get(vulnerabilities_endpoint, headers=HEADERS, params=params)

    if response.status_code == 200:
        vulnerabilities = response.json().get('data', [])
        if vulnerabilities:
            print(f"Vulnerabilities for Scan ID {scan_id}:")
            for vuln in vulnerabilities:
                vuln_id = vuln['id']
                severity = vuln['attributes'].get('severity', 'Unknown')
                description = vuln['attributes'].get('description', 'None')
                print(f"Vuln ID: {vuln_id}, Severity: {severity}, Description: {description}")
        else:
            print(f"No vulnerabilities found for Scan ID {scan_id}.")
    else:
        print(f"Failed to retrieve vulnerabilities for Scan ID {scan_id}. HTTP Status: {response.status_code}")
        print(response.text)

def main():
    # Replace with your actual scan IDs
    scan_ids = [
        "192a3cf4-2d95-4800-b131-607e566148fd",
        "8e7dc93e-7138-44df-ad61-0a779c568311"
    ]

    for scan_id in scan_ids:
        get_scan_vulnerabilities(scan_id)

if __name__ == "__main__":
    main()
