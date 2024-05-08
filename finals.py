import boto3
import requests

# Function to fetch the API key from AWS Secrets Manager
def get_api_key():
    # Create a Secrets Manager client
    client = boto3.client('secretsmanager')

    # Retrieve the secret value
    try:
        response = client.get_secret_value(SecretId='insightappsec/api-key')  # Replace 'your-secret-id' with the actual ARN or name of your secret
    except Exception as e:
        print("Failed to retrieve secret:", e)
        return None
    else:
        if 'SecretString' in response:
            secret = response['SecretString']
            return secret.get('api_key')
        else:
            print("Secret value is not a string.")
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
    else:
        print("Authentication failed. Status code:", response.status_code)

# Fetch API key from Secrets Manager
api_key = get_api_key()

# Validate API key
if api_key:
    validate_api_key(api_key)
else:
    print("API key retrieval failed.")
