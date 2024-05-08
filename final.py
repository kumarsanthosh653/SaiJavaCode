import subprocess
import json
import os
import requests

# Define the base URL for the API
base_url = 'https://us3.api.insight.rapid7.com'

# Endpoint for authentication validation
validate_endpoint = '/validate'

# Endpoint to create a new scan
create_scan_endpoint = '/ias/v1/scans'

# Function to retrieve API key from AWS Systems Manager Parameter Store
def get_api_key_from_parameter_store(param_name):
    try:
        # Execute AWS CLI command to retrieve parameter value
        command = f'aws ssm get-parameter --name {param_name} --with-decryption --query "Parameter.Value"'
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, text=True)
        # Parse and return the parameter value
        return result.stdout.strip()
    except Exception as e:
        print("Error retrieving parameter:", e)
        return None

# Function to perform authentication
def validate_api_key(api_key):
    # Construct the full URL for validation
    url = base_url + validate_endpoint

    # Define headers for authentication
    headers = {
        'X-Api-Key': api_key
    }

    # Make the GET request for validation
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Authentication successful!")
    else:
        print("Authentication failed. Status code:", response.status_code)

# Function to create a new scan
def create_scan(api_key):
    # Construct the full URL for creating a new scan
    url = base_url + create_scan_endpoint

    # Define headers for authentication
    headers = {
        'X-Api-Key': api_key
    }

    # Define the payload for the new scan
    payload = {
        "scan_config": {
            "id": "5fdaf09c-0eea-4324-8a7b-20ceb13365b9"
        },
        "scan_type": "REGULAR"
    }

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
    else:
        print("Failed to create new scan. Status code:", response.status_code)

# Function to check vulnerabilities
def check_vulnerabilities():
    # Perform any logic to check for vulnerabilities
    # For demonstration purposes, let's assume vulnerabilities are more than 1
    return True

# Retrieve API key from AWS Systems Manager Parameter Store
param_name = "ohana-apis"
api_key = get_api_key_from_parameter_store(param_name)

# Check if API key exists
if api_key:
    # Perform authentication
    validate_api_key(api_key)

    # Create a new scan
    create_scan(api_key)

    # Check for vulnerabilities
    if check_vulnerabilities():
        print("Vulnerabilities found! Breaking the pipeline.")
        raise Exception("Vulnerabilities found! Pipeline terminated.")
else:
    print("API key not found in Parameter Store. Please check your configuration.")




# import requests

# # Define your API key
# api_key = '801231d4-b4ae-42e4-ba2c-53ebe9ae02c6'

# # Define the base URL for the API
# base_url = 'https://us3.api.insight.rapid7.com'

# # Endpoint for authentication validation
# validate_endpoint = '/validate'

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

# # Function to create a new scan
# def create_scan():
#     # Construct the full URL for creating a new scan
#     url = base_url + create_scan_endpoint

#     # Define the payload for the new scan
#     payload = {
#         "scan_config": {
#             "id": "5fdaf09c-0eea-4324-8a7b-20ceb13365b9"
#         },
#         "scan_type": "REGULAR"
#     }

#     # Make the POST request to create a new scan
#     response = requests.post(url, json=payload, headers=headers)

#     # Check if the request was successful
#     if response.status_code == 201:
#         print("New scan created successfully!")
#         try:
#             json_response = response.json()
#             if json_response:
#                 print("Response:")
#                 print(json_response)
#             else:
#                 print("No response content.")
#         except ValueError:
#             print("Response is not valid JSON.")
#     else:
#         print("Failed to create new scan. Status code:", response.status_code)


# # Function to check vulnerabilities
# def check_vulnerabilities():
#     # Perform any logic to check for vulnerabilities
#     # For demonstration purposes, let's assume vulnerabilities are more than 1
#     return True
    
# # Perform authentication
# validate_api_key()

# # Create a new scan
# create_scan()

# # Check for vulnerabilities
# if check_vulnerabilities():
#     print("Vulnerabilities found! Breaking the pipeline.")
#     raise Exception("Vulnerabilities found! Pipeline terminated.")