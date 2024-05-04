import requests

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
    else:
        print("Failed to fetch scans. Status code:", response.status_code)

# Function to create a new scan
def create_scan():
    # Construct the full URL for creating a new scan
    url = base_url + create_scan_endpoint

    # Define the payload for the new scan (adjust as per your requirements)
    payload = {
        'name': 'New Scan Name',
        'target': 'https://example.com',
        # Add any other parameters required for the scan
    }

    # Make the POST request to create a new scan
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 201:
        print("New scan created successfully!")
        print("Response:")
        print(response.json())
    else:
        print("Failed to create new scan. Status code:", response.status_code)

# Perform authentication
validate_api_key()

# Fetch scans
fetch_scans()

# Create a new scan
create_scan()
