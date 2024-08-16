import requests

# Function to fetch vulnerabilities for a specific scan ID
def fetch_vulnerabilities(scan_id, api_key):
    url = "https://us2.api.insight.rapid7.com/ias/v1/vulnerabilities"
    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }
    params = {
        "scan.id": scan_id  # Ensure the correct scan ID is being used as a parameter
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        vulnerabilities = response.json().get('data', [])
        return vulnerabilities
    else:
        print(f"Failed to fetch vulnerabilities for Scan ID {scan_id}. Status Code: {response.status_code}")
        return []

# Function to display vulnerabilities for a given scan ID
def display_vulnerabilities(scan_id, vulnerabilities):
    print(f"Vulnerabilities for Scan ID {scan_id}:")
    for vuln in vulnerabilities:
        vuln_id = vuln.get('id', 'N/A')
        severity = vuln.get('severity', 'N/A')
        description = vuln.get('description', 'None')
        print(f"Vuln ID: {vuln_id}, Severity: {severity}, Description: {description}")

# List of scan IDs to test
scan_ids = [
    "192a3cf4-2d95-4800-b131-607e566148fd",
    "8e7dc93e-7138-44df-ad61-0a779c568311"
]

# Your API key
api_key = "your_api_key_here"

# Fetch and display vulnerabilities for each scan ID
for scan_id in scan_ids:
    vulnerabilities = fetch_vulnerabilities(scan_id, api_key)
    display_vulnerabilities(scan_id, vulnerabilities)
    print("\n" + "-"*50 + "\n")
