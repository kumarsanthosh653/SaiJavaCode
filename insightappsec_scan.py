import requests
import time
import yaml

# Load settings from the settings.yml file
with open("settings.yml", 'r') as file:
    settings = yaml.safe_load(file)

# Extract connection details and scan information
region = settings['connection']['region']
api_key = settings['connection']['api_key']
scan_info = settings['scan_info']
status_check_interval = settings['status_check_interval']

# InsightAppSec API base URL
base_url = f"https://{region}.api.insight.rapid7.com/ias/v1"

# Headers for API requests
headers = {
    'X-Api-Key': api_key,
    'Content-Type': 'application/json'
}

# Function to create a scan
def create_scan(app_name, scan_config_name):
    # Construct the scan creation payload
    payload = {
        "app": {"name": app_name},
        "scan_config": {"name": scan_config_name}
    }
    
    # Send a POST request to create the scan
    response = requests.post(f"{base_url}/scans", headers=headers, json=payload)
    
    if response.status_code == 201:
        scan_id = response.json().get('id')
        print(f"Scan created successfully with ID: {scan_id}")
        return scan_id
    else:
        print(f"Failed to create scan: {response.text}")
        return None

# Function to check the status of the scan and monitor for vulnerabilities
def check_scan_status(scan_id):
    while True:
        response = requests.get(f"{base_url}/scans/{scan_id}", headers=headers)
        
        if response.status_code == 200:
            scan_data = response.json()
            status = scan_data['status']
            print(f"Scan status: {status}")
            
            if status == "COMPLETE":
                print("Scan completed. Checking for vulnerabilities...")
                check_vulnerabilities(scan_id)
                break
        else:
            print(f"Failed to check scan status: {response.text}")
        
        time.sleep(status_check_interval)

# Function to check for vulnerabilities in the completed scan
def check_vulnerabilities(scan_id):
    response = requests.get(f"{base_url}/vulnerabilities?scan.id={scan_id}", headers=headers)
    
    if response.status_code == 200:
        vulnerabilities = response.json().get('data', [])
        
        high_severity_found = any(vuln['severity'] == 'HIGH' for vuln in vulnerabilities)
        low_severity_found = any(vuln['severity'] == 'LOW' for vuln in vulnerabilities)
        
        if high_severity_found or low_severity_found:
            print("Vulnerabilities detected:")
            for vuln in vulnerabilities:
                if vuln['severity'] in ['HIGH', 'LOW']:
                    print(f"- {vuln['title']} (Severity: {vuln['severity']})")
            print("Immediate attention required!")
        else:
            print("No high or low severity vulnerabilities detected.")
    else:
        print(f"Failed to retrieve vulnerabilities: {response.text}")

# Main function to execute the scan and monitor results
def main():
    for scan in scan_info:
        app_name = scan['app_name']
        scan_config_name = scan['scan_config_name']
        
        scan_id = create_scan(app_name, scan_config_name)
        
        if scan_id:
            check_scan_status(scan_id)

if __name__ == "__main__":
    main()
