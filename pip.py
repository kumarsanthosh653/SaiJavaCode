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
        return response.json()  # Return the JSON response
    else:
        print("Failed to fetch scans. Status code:", response.status_code)
        return None

# Function to create a new scan
def create_scan():
    # Get the list of scans
    scans = fetch_scans()
    if scans is None:
        return  # Exit if fetching scans failed

    # Extract the parent_scan_id based on the scan_config ID
    scan_config_id = "5fdaf09c-0eea-4324-8a7b-20ceb13365b9"  # Replace with your desired scan_config ID
    parent_scan_id = None
    for scan in scans.get("data", []):
        if scan.get("scan_config", {}).get("id") == scan_config_id:
            parent_scan_id = scan.get("id")
            break

    if parent_scan_id is None:
        print(f"No scan found with scan_config ID {scan_config_id}")
        return

    # Construct the full URL for creating a new scan
    url = base_url + create_scan_endpoint

    # Define the payload for the new scan
    payload = {
        "scan_config": {
            "id": scan_config_id
        },
        "scan_type": "VERIFICATION",
        "validation": {
            "parent_scan_id": parent_scan_id
        }
        # Add any other parameters required for the scan
    }

    # Make the POST request to create a new scan
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 201:
        print("New scan created successfully!")
        # Check if the response content is empty
        if response.text:
            print("Response:")
            print(response.json())
        else:
            print("No response content.")
    else:
        print("Failed to create new scan. Status code:", response.status_code)

# Perform authentication
validate_api_key()

# Create a new scan
create_scan()



# import requests

# # Define your API key
# api_key = '801231d4-b4ae-42e4-ba2c-53ebe9ae02c6'

# # Define the base URL for the API
# base_url = 'https://us3.api.insight.rapid7.com'

# # Endpoint for authentication validation
# validate_endpoint = '/validate'

# # Endpoint to fetch scans
# scans_endpoint = '/ias/v1/scans'

# # Endpoint to create a new scan
# create_scan_endpoint = '/ias/v1/scans'

# # Define headers for authentication
# headers = {
#     'X-Api-Key': api_key
# }

# # Function to perform authentication
# def validate_api_key():
#     # Construct the full URL for validation
#     url = base_url + validate_endpoint

#     # Make the GET request for validation
#     response = requests.get(url, headers=headers)

#     # Check if the request was successful
#     if response.status_code == 200:
#         print("Authentication successful!")
#     else:
#         print("Authentication failed. Status code:", response.status_code)

# # Function to fetch scans
# def fetch_scans():
#     # Construct the full URL for fetching scans
#     url = base_url + scans_endpoint

#     # Make the GET request to fetch scans
#     response = requests.get(url, headers=headers)

#     # Check if the request was successful
#     if response.status_code == 200:
#         print("Scans fetched successfully!")
#         print("Response:")
#         print(response.json())
#     else:
#         print("Failed to fetch scans. Status code:", response.status_code)

# # Function to create a new scan
# def create_scan():
#     # Construct the full URL for creating a new scan
#     url = base_url + create_scan_endpoint

#     # Define the payload for the new scan (adjust as per your requirements)
#     payload = {
#         "scan_config": {
#             "id": "5fdaf09c-0eea-4324-8a7b-20ceb13365b9"
#         },
#         "scan_type": "VERIFICATION",
#         "validation": {
#             "parent_scan_id": "fecf4e8e-1a32-401a-bba3-06c5d7200483"
#         }
#         # Add any other parameters required for the scan
#     }

#     # Make the POST request to create a new scan
#     response = requests.post(url, json=payload, headers=headers)

#     # Check if the request was successful
#     if response.status_code == 201:
#         print("New scan created successfully!")
#         # Check if the response content is empty
#         if response.text:
#             print("Response:")
#             print(response.json())
#         else:
#             print("No response content.")
#     else:
#         print("Failed to create new scan. Status code:", response.status_code)

# # Perform authentication
# validate_api_key()

# # Fetch scans
# fetch_scans()

# # Create a new scan
# create_scan()
