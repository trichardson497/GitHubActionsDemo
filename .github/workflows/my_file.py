# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 10:39:15 2024

@author: TobyRichardson
"""

import requests
import json

# Define the URL and API key
url = "https://presales.testinsights.io:443/api/apikey/qveP5Ml1Xvr1NP0MkEXv_9fBF/job"

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
            {"var": "parUserID", "paramIndex": 1, "value": 71},
            {"var": "parAccountType", "paramIndex": 2, "value": "Individual Savings"},
            {"var": "parTargetConnectionID", "paramIndex": 3, "value": "1"},
            {"var": "paritem_account_number_seq_", "paramIndex": 4, "value": "1"},
            {"var": "parExportCSV_account_", "paramIndex": 5, "value": "false"},
            {"var": "parExportCSV_account_number_seq_", "paramIndex": 6, "value": "false"}
        ],
        "sharedJobServer": False
    }
}

# Define headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")
