import boto3

import requests
 
# Retrieve API key from Secrets Manager

client = boto3.client('secretsmanager')

secret_value = client.get_secret_value(SecretId="insightappsec/api-key")['SecretString']

api_key = secret_value.strip()
 
# Replace with the Insightappsec API endpoint URL for triggering a scan

url = "https://us3.api.insight.rapid7.com/ias/v1/"
 
# Replace with your application ID or other relevant data for the scan request

data = {

    "target": "29380e15-ebfa-4417-b770-a362d2869898",

    # Add other scan configuration options as needed

}
 
headers = {

    "Authorization": f"Token {api_key}"

}
 
response = requests.post(url, headers=headers, json=data)
 
# Handle the API response (e.g., print status code, parse JSON for scan details)

print(f"API Response Status Code: {response.status_code}")

# ... Parse response data if needed
 
