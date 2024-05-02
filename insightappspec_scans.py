import boto3
import requests

# Retrieve API key from Secrets Manager
client = boto3.client('secretsmanager')
secret_value = client.get_secret_value(SecretId="insightappsec/api-key")['SecretString']
api_key = secret_value.strip()

# Define the InsightAppSec API endpoint URL for triggering a scan
url = "https://us.api.insight.rapid7.com/ias/v1/scans"

# Replace 'target' with your application ID or other relevant data for the scan request
data = {
    "target": "29380e15-ebfa-4417-b770-a362d2869898",
    # Add other scan configuration options as needed
}

headers = {
    "Authorization": f"Token {api_key}"
}

# Send a POST request to trigger the scan
response = requests.post(url, headers=headers, json=data)

# Handle the API response
print(f"API Response Status Code: {response.status_code}")

if response.status_code == 200:
    print("Scan successfully triggered.")
    # Parse response data for scan details
    scan_id = response.json().get('id')
    print(f"Scan ID: {scan_id}")
else:
    print("Failed to trigger the scan. Error:", response.text)

# If the scan was successfully triggered, you can now retrieve scan results, for example:
if scan_id:
    scan_results_url = f"https://us.api.insight.rapid7.com/ias/v1/scans/{scan_id}/results"
    scan_results_response = requests.get(scan_results_url, headers=headers)
    if scan_results_response.status_code == 200:
        print("Scan results:")
        print(scan_results_response.json())
    else:
        print("Failed to fetch scan results. Error:", scan_results_response.text)
