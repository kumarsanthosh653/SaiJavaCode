import requests

# Define your API key
api_key = '801231d4-b4ae-42e4-ba2c-53ebe9ae02c6'

# Define the base URL for the API
base_url = 'https://us3.api.insight.rapid7.com'

# Endpoint for authentication validation
validate_endpoint = '/validate'

# Endpoint to create scans
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

# Function to create a scan using a scan configuration ID
def create_scan(scan_config_id):
    # Construct the full URL for creating a scan
    url = base_url + create_scan_endpoint

    # Define the payload for creating a scan
    payload = {
        "scan_config": {
            "id": "5fdaf09c-0eea-4324-8a7b-20ceb13365b9"
        },
        "scan_type": "REGULAR"
    }

    # Make the POST request to create a scan
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 201:
        print("Scan created successfully!")
        print("Response:")
        print(response.json())
    else:
        print("Failed to create scan. Status code:", response.status_code)

# Perform authentication
validate_api_key()

# Provide the scan configuration ID and create a scan
scan_config_id = 'your_scan_config_id_here'
create_scan(scan_config_id)
