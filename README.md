# Test Insights API Client

A Python client for interacting with the Test Insights API. This tool provides an interface to perform operations via the API, with some features still under development.

## Features

Query job engine operations via the Test Insights API.
Swagger documentation for reference: API Documentation.

**Note**: The data endpoint is currently non-functional. Updates will be provided once it's operational.

## Prerequisites

Before you start, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/test-insights-python-client.git
cd test-insights-python-client
```

### 2. Set up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### 3. Install Dependencies

Install the required libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Run the Script

After installing the dependencies, you can run the main Python script:

```bash
python main.py
```

### 2. Configuration

- API base URL: Ensure the base URL is correctly set in the script (default: `https://presales.testinsights.io/api`).
- Authentication: Add any required API keys or tokens in the designated configuration section of `main.py`.

### 3. Example API Request

```python
from api_client import TestInsightsAPI

client = TestInsightsAPI(base_url="https://presales.testinsights.io/api")
response = client.get_job_engine_status()
print(response)
```

## Development Notes

- **Data Endpoint**: The `data` endpoint is currently under construction and will be supported in future updates.
- **Dependencies**: If you add new libraries during development, update the `requirements.txt` file using:

```bash
pip freeze > requirements.txt
```