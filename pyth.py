import requests
import time

# Define your API key
api_key = '801231d4-b4ae-42e4-ba2c-53ebe9ae02c6'

# Define the base URL for the API
base_url = 'https://us3.api.insight.rapid7.com'

# Endpoint for authentication validation
validate_endpoint = '/validate'

# Endpoint to fetch scans
scans_endpoint = '/ias/v1/scans'

# Endpoint to create a new scan
create_scan_endpoint = '/ias/v1/scans'

# Define headers for authentication
headers = {
    'X-Api-Key': api_key
}

# Function to perform authentication
def validate_api_key():
    # Construct the full URL for validation
    url = base_url + validate_endpoint

    # Make the GET request for validation
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Authentication successful!")
    else:
        print("Authentication failed. Status code:", response.status_code)

# Function to fetch scans
def fetch_scans():
    # Construct the full URL for fetching scans
    url = base_url + scans_endpoint

    # Make the GET request to fetch scans
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Scans fetched successfully!")
        print("Response:")
        print(response.json())
        return response.json()
    else:
        print("Failed to fetch scans. Status code:", response.status_code)
        return None

# Function to create a new scan
def create_scan(parent_scan_id):
    # Construct the full URL for creating a new scan
    url = base_url + create_scan_endpoint

    # Define the payload for the new scan
    payload = {
        "scan_config": {
            "id": "5fdaf09c-0eea-4324-8a7b-20ceb13365b9"
        },
        "scan_type": "VERIFICATION",
        "validation": {
            "parent_scan_id": parent_scan_id
        }
    }

    # Make the POST request to create a new scan
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 201:
        print("New scan created successfully!")
        try:
            scan_id = response.json().get('id')
            if scan_id:
                print("Scan ID:", scan_id)
                return scan_id
            else:
                print("Failed to retrieve scan ID from response.")
                return None
        except Exception as e:
            print("Failed to parse response JSON:", e)
            return None
    else:
        print("Failed to create new scan. Status code:", response.status_code)
        return None

# Perform authentication
validate_api_key()

# Fetch scans
scan_results = fetch_scans()

if scan_results:
    for scan in scan_results.get('data', []):
        vulnerabilities_count = 0
        # Check if there are any vulnerabilities
        if vulnerabilities_count >= 3:
            print("Vulnerabilities found. Breaking the pipeline.")
            break
        parent_scan_id = scan.get('validation', {}).get('parent_scan_id')
        # Create a new scan with the parent_scan_id
        scan_id = create_scan(parent_scan_id)
        if scan_id:
            # Wait for some time before fetching next scan
            time.sleep(10)
        else:
            print("Failed to create scan. Skipping to the next one.")
else:
    print("No scans fetched. Exiting.")
