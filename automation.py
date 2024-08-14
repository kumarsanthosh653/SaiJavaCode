import boto3
import json
import requests

# Function to fetch the API key from AWS Systems Manager Parameter Store
def get_api_key():
    ssm = boto3.client('ssm')
    try:
        response = ssm.get_parameter(Name='/insightappsec/apikey', WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as e:
        print("Failed to retrieve parameter:", e)
        return None

# Function to perform authentication
def validate_api_key(api_key):
    base_url = 'https://us3.api.insight.rapid7.com'
    validate_endpoint = '/validate'
    headers = {'X-Api-Key': api_key}
    url = base_url + validate_endpoint
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Authentication successful!")
        return True
    else:
        print("Authentication failed. Status code:", response.status_code)
        return False

# Function to create a new scan
def create_scan(api_key):
    base_url = 'https://us3.api.insight.rapid7.com'
    create_scan_endpoint = '/ias/v1/scans'
    headers = {'X-Api-Key': api_key, 'Content-Type': 'application/json'}
    payload = {
        "scan_config": {"id": "2d01b271-151f-42dd-a65f-56d50de7cdd3"},
        "scan_type": "REGULAR"
    }
    url = base_url + create_scan_endpoint
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("New scan created successfully!")
        try:
            json_response = response.json()
            if json_response:
                print("Response:")
                print(json_response)
                # Check for vulnerabilities
                check_vulnerabilities(api_key, json_response.get('scan_id'))
            else:
                print("No response content.")
        except ValueError:
            print("Response is not valid JSON.")
    else:
        print("Failed to create new scan. Status code:", response.status_code)

# Function to check vulnerabilities and display messages based on severity
def check_vulnerabilities(api_key, scan_id):
    base_url = 'https://us3.api.insight.rapid7.com'
    vulnerabilities_endpoint = f'/ias/v1/scans/{scan_id}/vulnerabilities'
    headers = {'X-Api-Key': api_key}
    url = base_url + vulnerabilities_endpoint
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        vulnerabilities = response.json()
        if vulnerabilities:
            for vulnerability in vulnerabilities.get('items', []):
                severity = vulnerability.get('severity')
                description = vulnerability.get('description', 'No description available')
                if severity in ['High', 'Low']:
                    print(f"Vulnerability detected with {severity} severity!")
                    print(f"Description: {description}")
                    # Prompt for immediate attention
                    prompt_attention(severity, description)
        else:
            print("No vulnerabilities found.")
    else:
        print("Failed to check vulnerabilities. Status code:", response.status_code)

# Function to prompt for immediate attention based on severity
def prompt_attention(severity, description):
    print(f"Immediate Attention Required!")
    print(f"Severity: {severity}")
    print(f"Description: {description}")

# Fetch API key from Systems Manager Parameter Store
api_key = get_api_key()

# Validate API key
if api_key and validate_api_key(api_key):
    # If API key is valid, create a new scan and check for vulnerabilities
    create_scan(api_key)
else:
    print("API key retrieval or validation failed.")
