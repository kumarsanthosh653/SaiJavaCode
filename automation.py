import boto3
import json
import requests

# Function to fetch the API key from AWS Systems Manager Parameter Store
def get_api_key():
    # Create an SSM client
    ssm = boto3.client('ssm')

    # Retrieve the parameter value
    try:
        response = ssm.get_parameter(Name='/ohana-api/appspec-insights/api-key', WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as e:
        print("Failed to retrieve parameter:", e)
        return None

# Function to perform authentication
def validate_api_key(api_key):
    base_url = 'https://us3.api.insight.rapid7.com'
    validate_endpoint = '/validate'
    headers = {
        'X-Api-Key': api_key
    }

    # Construct the full URL for validation
    url = base_url + validate_endpoint

    # Make the GET request for validation
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Authentication successful!")
        return True
    else:
        print("Authentication failed. Status code:", response.status_code)
        return False

# Function to create a new scan
def create_scan(api_key):
    base_url = 'https://us3.api.insight.rapid7.com'
    create_scan_endpoint = '/ias/v1/scans'  # Replace with the actual endpoint for creating a scan

    headers = {
        'X-Api-Key': api_key,
        'Content-Type': 'application/json'
    }

    # Define the payload for the new scan
    payload = {
        "scan_config": {
            "id": "6634fd2f-91f3-4e0a-ab5a-e83741ca5f8a"  # Replace with your actual scan configuration ID
        },
        "scan_type": "REGULAR"
    }

    # Construct the full URL for creating a new scan
    url = base_url + create_scan_endpoint

    # Make the POST request to create a new scan
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 201:
        print("New scan created successfully!")
        try:
            json_response = response.json()
            if json_response:
                print("Response:")
                print(json_response)
                scan_id = json_response.get("scan_id")
                if scan_id:
                    return scan_id
                else:
                    print("Scan ID not found in response.")
                    return None
            else:
                print("No response content.")
                return None
        except ValueError:
            print("Response is not valid JSON.")
            return None
    else:
        print("Failed to create new scan. Status code:", response.status_code)
        return None

# Function to check vulnerabilities and provide details
def check_vulnerabilities(api_key, scan_id):
    base_url = 'https://us3.api.insight.rapid7.com'
    get_vulnerabilities_endpoint = f'/ias/v1/scans/{scan_id}/vulnerabilities'

    headers = {
        'X-Api-Key': api_key
    }

    # Construct the full URL for retrieving vulnerabilities
    url = base_url + get_vulnerabilities_endpoint

    # Make the GET request to retrieve vulnerabilities
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            vulnerabilities = response.json().get("vulnerabilities", [])
            if vulnerabilities:
                print(f"Total vulnerabilities found: {len(vulnerabilities)}")
                vulnerability_types = set(vuln["type"] for vuln in vulnerabilities)
                print("Vulnerability types found:")
                for vuln_type in vulnerability_types:
                    print(f"- {vuln_type}")
            else:
                print("No vulnerabilities found.")
        except ValueError:
            print("Response is not valid JSON.")
    else:
        print("Failed to retrieve vulnerabilities. Status code:", response.status_code)

# Fetch API key from Systems Manager Parameter Store
api_key = get_api_key()

# Validate API key
if api_key and validate_api_key(api_key):
    # If API key is valid, create a new scan and check for vulnerabilities
    scan_id = create_scan(api_key)
    if scan_id:
        check_vulnerabilities(api_key, scan_id)
else:
    print("API key retrieval or validation failed.")

