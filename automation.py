import boto3
import json
import requests
from requests.auth import HTTPBasicAuth

# Configuration for JIRA
JIRA_BASE_URL = 'https://kumarsanthosh653.atlassian.net'
JIRA_PROJECT_KEY = 'KAN'
JIRA_USER_EMAIL = 'kumarsanthosh653@gmail.com'
JIRA_API_TOKEN = 'ATATT3xFfGF0k1qdgA_PSCrFEJ7bJ5WlunSmuWjQcdFrrG0mUFrvxzdoxha7HasD3dd8zF8up7nFL8tcuue9nkakKRAfkDJmoqL2nOSzcGEjBbzVU7DZ0FMQvNsRy0gcg-cJfc7wmPvlpwjpr4Adl_151NDvxzXYOiRXfaG6XSeiW2Q2yDFNt4U=CD90DFF0'  # Store securely

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

    # Print full response content for debugging
    print(f"Response Content: {response.content}")

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
        print(f"Failed to create new scan. Status code: {response.status_code}, Content: {response.content}")
        return None

# Function to create a JIRA issue
def create_jira_issue(summary, description, priority):
    url = f'{JIRA_BASE_URL}/rest/api/3/issue'
    auth = HTTPBasicAuth(JIRA_USER_EMAIL, JIRA_API_TOKEN)
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Prepare the payload for creating a JIRA issue
    issue_data = {
        'fields': {
            'project': {
                'key': JIRA_PROJECT_KEY
            },
            'summary': summary,
            'description': description,
            'issuetype': {
                'name': 'Bug'  # Change as needed
            },
            'priority': {
                'name': priority
            }
        }
    }

    # Make the POST request to create a JIRA issue
    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(issue_data))

    # Check if the request was successful
    if response.status_code == 201:
        print(f'Issue created successfully: {response.json()["key"]}')
    else:
        print(f'Failed to create issue: {response.content}')

# Function to check vulnerabilities and create JIRA issues
def check_vulnerabilities_and_create_issues(api_key, scan_id):
    base_url = 'https://us3.api.insight.rapid7.com'
    get_vulnerabilities_endpoint = f'/ias/v1/scans/{scan_id}/vulnerabilities'

    headers = {
        'X-Api-Key': api_key
    }

    # Construct the full URL for retrieving vulnerabilities
    url = base_url + get_vulnerabilities_endpoint

    # Make the GET request to retrieve vulnerabilities
    response = requests.get(url, headers=headers)

    # Print full response content for debugging
    print(f"Response Content: {response.content}")

    # Check if the request was successful
    if response.status_code == 200:
        try:
            vulnerabilities = response.json().get("vulnerabilities", [])
            if vulnerabilities:
                print(f"Total vulnerabilities found: {len(vulnerabilities)}")
                for vuln in vulnerabilities:
                    summary = vuln.get('title', 'Vulnerability')
                    description = vuln.get('description', 'No description available.')
                    priority = vuln.get('severity', 'Medium')  # Map severity to JIRA priority if needed
                    create_jira_issue(summary, description, priority)
            else:
                print("No vulnerabilities found.")
        except ValueError:
            print("Response is not valid JSON.")
    else:
        print(f"Failed to retrieve vulnerabilities. Status code: {response.status_code}, Content: {response.content}")

# Fetch API key from Systems Manager Parameter Store
api_key = get_api_key()

# Validate API key
if api_key and validate_api_key(api_key):
    # If API key is valid, create a new scan and check for vulnerabilities
    scan_id = create_scan(api_key)
    if scan_id:
        check_vulnerabilities_and_create_issues(api_key, scan_id)
else:
    print("API key retrieval or validation failed.")
