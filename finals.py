import json
import requests

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
    else:
        print("Authentication failed. Status code:", response.status_code)

# Read API key from secret.json
try:
    with open('secret.json', 'r') as file:
        secret_data = json.load(file)
        api_key = secret_data.get('api_key')
except Exception as e:
    print("Failed to read secret:", e)
    api_key = None

# Validate API key
if api_key:
    validate_api_key(api_key)
else:
    print("API key retrieval failed.")
