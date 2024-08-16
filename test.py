import requests
import json
import logging

class InsightAppSecClient:
    def __init__(self, api_key, region):
        self.url = f'https://{region}.api.insight.rapid7.com/ias/v1'
        self.headers = {
            'X-Api-Key': api_key,
            'Content-Type': 'application/json'
        }

    def search(self, search_type, query):
        url = self.url + "/search"
        headers = self.headers
        body = {
            "type": search_type,
            "query": query
        }
        cont = True
        results = []

        try:
            while cont:
                response = requests.post(url=url, headers=headers, data=json.dumps(body))
                response.raise_for_status()

                response_dict = response.json()
                results.extend(response_dict.get("data", []))

                # Pagination handling
                if len(results) >= response_dict.get("metadata", {}).get("total_data", 0):
                    cont = False
                else:
                    # Move to the next page
                    next_link = None
                    for link in response_dict.get("links", []):
                        if link.get("rel") == "next":
                            next_link = link.get("href")
                            break
                    if next_link:
                        url = next_link
                    else:
                        cont = False

            return results
        except Exception as e:
            logging.error("Error in InsightAppSec API: Search", exc_info=e)
            raise e

# Example usage
if __name__ == "__main__":
    # Replace with your actual API key and region
    api_key = 'f8096810-123c-43c9-87c8-cc76cebea7ec'
    region = 'us'
    
    # Instantiate the client
    client = InsightAppSecClient(api_key=api_key, region=region)
    
    # Search for vulnerabilities related to a specific scan ID
    search_type = "VULNERABILITY"
    query = "scan.id:a23742bc-c5c2-4c27-b3a2-fe2ee5c9b95b"
    
    try:
        vulnerabilities = client.search(search_type=search_type, query=query)
        for vuln in vulnerabilities:
            print(f"ID: {vuln.get('id')}")
            print(f"Title: {vuln.get('title')}")
            print(f"Severity: {vuln.get('severity')}")
            print(f"Description: {vuln.get('description')}")
            print("-" * 40)
    except Exception as e:
        print(f"An error occurred: {e}")
