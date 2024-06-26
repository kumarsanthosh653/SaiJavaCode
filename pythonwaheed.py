import boto3
import json
import requests

# Function to fetch the API key from AWS Systems Manager Parameter Store
def get_api_key():
    # Create an SSM client
    ssm = boto3.client('ssm')

    # Retrieve the parameter value
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
            "id": "5fdaf09c-0eea-4324-8a7b-20ceb13365b9"
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
            else:
                print("No response content.")
        except ValueError:
            print("Response is not valid JSON.")

        # Check for vulnerabilities
        if check_vulnerabilities():
            print("Vulnerabilities found! Failing the pipeline.")
            raise Exception("Vulnerabilities found! Pipeline terminated.")
    else:
        print("Failed to create new scan. Status code:", response.status_code)

# Placeholder function to check vulnerabilities (always returns True for demonstration)
def check_vulnerabilities():
    # Perform any logic to check for vulnerabilities
    # For demonstration purposes, let's assume vulnerabilities are found
    return True

# Fetch API key from Systems Manager Parameter Store
api_key = get_api_key()

# Validate API key
if api_key and validate_api_key(api_key):
    # If API key is valid, create a new scan and check for vulnerabilities
    create_scan(api_key)
else:
    print("API key retrieval or validation failed.")
