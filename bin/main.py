import sys
sys.path.append("..")
import os
from ruamel.yaml import YAML
from datetime import datetime
from lib.helpers import scan_automation
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_ssm_parameter(name):
    ssm_client = boto3.client('ssm')
    try:
        response = ssm_client.get_parameter(Name=name, WithDecryption=True)
        return response['Parameter']['Value']
    except ssm_client.exceptions.ParameterNotFound:
        print(f"Parameter {name} not found")
        raise
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"AWS credentials not found or incomplete: {e}")
        raise
    except Exception as e:
        print(f"Error retrieving parameter {name}: {e}")
        raise

def main():
    # Load configuration file
    yaml = YAML(typ='safe')
    settings = yaml.load(open("../config/settings.yml"))
    
    # Get connection info
    if settings.get("connection"):
        api_key = get_ssm_parameter("/ohana-api/appspec-insights/api-key")
        region = settings.get("connection").get("region", "us")
    else:
        api_key = None
        region = "us"

    print(f"Region: {region}")
    scan_automation.create_scan(api_key, region, settings)

if __name__ == "__main__":
    main()
