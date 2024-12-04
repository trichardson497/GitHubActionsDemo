# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 10:39:15 2024

@author: TobyRichardson
"""

import requests
import json
import time
import zipfile
import os
import pandas as pd

# Common Configuration
API_KEY = "qveP5Ml1Xvr1NP0MkEXv_9fBF"  # TODO: Load from environment variable
BASE_URL = f"https://presales.testinsights.io/api/apikey/{API_KEY}"
HEADERS = {"Content-Type": "application/json"}

def submit_job(user_id, account_type, num_accounts):
    """
    Submits a job with the given parameters.
    """
    # Define the payload
    payload = {
        "jobType": "VIPAutoExecutionJob",
        "projectId": 100003,
        "vipAutomationJobSettings": {
            "testSuiteId": None,
            "testPaths": None,
            "machineKey": "EC2AMAZ-0L04NIQ",
            "serverProfileId": 2,
            "serverProcessId": 536,
            "automationType": "Generate Accounts for current user",
            "scope": "Global",
            "automationParameters": [
                {"var": "parUserID", "paramIndex": 1, "value": user_id},
                {"var": "parAccountType", "paramIndex": 2, "value": account_type},
                {"var": "parTargetConnectionID", "paramIndex": 3, "value": "1"},
                {"var": "paritem_account_number_seq_", "paramIndex": 4, "value": num_accounts},
                {"var": "parExportCSV_account_", "paramIndex": 5, "value": "true"},
                {"var": "parExportCSV_account_number_seq_", "paramIndex": 6, "value": "false"}
            ],
            "sharedJobServer": False
        }
    }

    # Submit the job
    response = requests.post(f"{BASE_URL}/job", headers=HEADERS, data=json.dumps(payload))
    if response.status_code != 200:
        print(f"Failed to submit job. Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return None

    # Parse the job ID from the response
    job_data = response.json()
    job_id = job_data.get("id")
    if not job_id:
        print("Job ID not found in the response.")
        return None

    print(f"Job submitted successfully. Job ID: {job_id}")
    return job_id


def poll_job_status(job_id, poll_interval=10):
    """
    Polls the job status until completion or failure.
    """
    status_url = f"{BASE_URL}/job/{job_id}"
    print("Polling for job status...")

    while True:
        status_response = requests.get(status_url, headers=HEADERS)
        if status_response.status_code != 200:
            print(f"Failed to get job status. Status Code: {status_response.status_code}")
            print(f"Response Text: {status_response.text}")
            return None

        status_data = status_response.json()
        job_state = status_data.get("jobState")
        print(f"Current Job State: {job_state}")

        if job_state == "Complete":
            print("Job completed successfully!")
            return True
        elif job_state in ["Error", "Cancelled"]:
            print(f"Job failed with state: {job_state}")
            return False

        time.sleep(poll_interval)


def retrieve_job_result(job_id):
    """
    Retrieves the result of the completed job.
    """
    result_url = f"{BASE_URL}/job/{job_id}/result"
    print("Retrieving job result...")
    result_response = requests.get(result_url, headers=HEADERS)
    if result_response.status_code != 200:
        print(f"Failed to get job result. Status Code: {result_response.status_code}")
        print(f"Response Text: {result_response.text}")
        return None

    result_data = result_response.json()
    print("Job Result:")
    print(json.dumps(result_data, indent=4))
    return result_data


    result_data_url = f"{BASE_URL}/job/{job_id}/data"
    print(f"Downloading job result data from {result_data_url}...")

    result_data_response = requests.get(result_data_url, headers=HEADERS, stream=True)
    if result_data_response.status_code != 200:
        print(f"Failed to download job result data. Status Code: {result_data_response.status_code}")
    print(f"Response Text: {result_data_response.text}")
    return False

    # Save the content as a zip file
    with open(save_path, "wb") as file:
        for chunk in result_data_response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    print(f"Job result data saved to {save_path}")
    return True

def download_result_data(result_id, save_path="result.zip"):
    """
    Downloads the result data using the result ID and saves it as a zip file.
    """
    result_data_url = f"{BASE_URL}/job/result/{result_id}/data"
    print(f"Downloading result data from {result_data_url}...")

    try:
        response = requests.get(result_data_url, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Failed to download result data. Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            return False

        # Save the content as a zip file
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # Filter out keep-alive chunks
                    file.write(chunk)

        print(f"Result data saved successfully to {save_path}")
        return True

    except Exception as e:
        print(f"An error occurred while downloading the result data: {e}")
        return False


def extract_and_list_ids(zip_path, target_csv_column="id"):
    """
    Extracts a ZIP file, finds the CSV, and lists the values of the specified column.
    """
    try:
        # Extract the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            extract_dir = zip_path.replace(".zip", "")
            zip_ref.extractall(extract_dir)

        # Find the CSV file
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                if file.endswith(".csv"):
                    csv_path = os.path.join(root, file)

                    # Read the CSV and get the IDs
                    df = pd.read_csv(csv_path)
                    if target_csv_column in df.columns:
                        ids = df[target_csv_column].to_list()
                        print(f"Created the following account IDs: {', '.join(map(str, ids))}")
                        return
                    else:
                        print(f"Column '{target_csv_column}' not found in CSV.")
                    return

        print("No CSV file found in the extracted folder.")

    except Exception as e:
        print(f"An error occurred: {e}")


# Main Execution
if __name__ == "__main__":
    # Parameters
    user_id = 71  # User ID to create accounts for
    account_type = "Individual Savings"  # Account type
    num_accounts = 1  # Number of accounts to create

    # Submit job
    job_id = submit_job(user_id, account_type, num_accounts)
    if not job_id:
        exit()

    # Poll job status
    if not poll_job_status(job_id):
        exit()

    # Retrieve job result
    result_data = retrieve_job_result(job_id)
    if not result_data:
        exit()

    # Extract result ID from the retrieved result data
    result_id = result_data.get("id")
    if not result_id:
        print("Result ID not found in the job result response.")
        exit()

    # Download and save job result data as a zip file using the result ID
    save_path = "job_result.zip"
    if not download_result_data(result_id, save_path):
        exit()

    # Extract and list IDs from the downloaded ZIP file
    extract_and_list_ids(save_path, target_csv_column="id")
