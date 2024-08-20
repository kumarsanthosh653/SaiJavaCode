import json
import requests


class InsightAppSec:
    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.api_key = kwargs.get("api_key")
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }

    def submit_scan(self, body):
        url = self.url + "/scans"
        try:
            response = requests.post(url=url, headers=self.headers, data=json.dumps(body))
            response.raise_for_status()

            scan_id = self.get_url_id(response.headers.get("location"))
            print(f"Launched new scan: {scan_id}")
            return scan_id
        except Exception as e:
            print(f"Error in InsightAppSec API: Submit Scan\n{e}")
            raise e

    def get_scan(self, scan_id):
        url = self.url + f"/scans/{scan_id}"
        try:
            response = requests.get(url=url, headers=self.headers)
            response.raise_for_status()

            return response.json()
        except Exception as e:
            print("Error in InsightAppSec API: Get Scan", e)
            raise e

    def search(self, search_type, query):
        url = self.url + "/search"
        body = {
            "type": search_type,
            "query": query
        }
        results = []

        try:
            while True:
                response = requests.post(url=url, headers=self.headers, data=json.dumps(body))
                response.raise_for_status()

                response_dict = response.json()
                results.extend(response_dict.get("data"))

                if len(results) >= response_dict.get("metadata").get("total_data"):
                    break
                else:
                    for link in response_dict.get("links"):
                        if link.get("rel") == "next":
                            url = link.get("href")
                            break
            return results
        except Exception as e:
            print("Error in InsightAppSec API: Search", e)
            raise e

    def get_url_id(self, url):
        return url.split("/")[-1]

    def get_vulnerabilities(self, scan_id):
        query = f"vulnerability.scans.id = '{scan_id}'"
        url = self.url + "/search"
        body = {
            "query": query,
            "type": "VULNERABILITY"
        }
        try:
            response = requests.post(url=url, headers=self.headers, data=json.dumps(body))
            response.raise_for_status()

            return response.json()
        except Exception as e:
            print(f"Error in InsightAppSec API: Get Vulnerabilities\n{e}")
            raise e
