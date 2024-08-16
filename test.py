import requests
import logging

class InsightAppSec:
    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.api_key = kwargs.get("api_key")
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }

    def get_vulnerabilities(self, scan_id):
        url = self.url + f"/vulnerabilities?query=vulnerability.scans.id='{scan_id}'"
        headers = self.headers

        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()

            vulnerabilities = response.json()
            return vulnerabilities
        except Exception as e:
            logging.error(f"Error in InsightAppSec API: Get Vulnerabilities\n{e}")
            raise e

def test_get_vulnerabilities():
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Replace with your actual API key and region
    api_key = "143c2a7a-534f-4daa-b58f-62b01db46def"
    region = "us2"
    scan_id = "1d3068a5-ac65-46b6-8008-2d2745950914"

    # Create an instance of InsightAppSec
    url = f"https://{region}.api.insight.rapid7.com/ias/v1"
    api = InsightAppSec(url=url, api_key=api_key)

    # Call the get_vulnerabilities method
    vulnerabilities = api.get_vulnerabilities(scan_id)

    # Print the results
    print(f"Vulnerabilities for Scan ID {scan_id}:")
    for vuln in vulnerabilities.get("data", []):
        vuln_id = vuln.get("id")
        severity = vuln.get("severity")
        description = vuln.get("description")
        print(f"Vuln ID: {vuln_id}, Severity: {severity}, Description: {description}")

if __name__ == "__main__":
    test_get_vulnerabilities()
