import json
import sys
# from tqdm import tqdm
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from google.oauth2 import service_account
from config import PATHS, BIGQUERY_VARIABLES
from credentials import get_credentials_path
from googleapiclient.discovery import build
from google.cloud.exceptions import NotFound as PROJECT_NOTFOUND


# Load credentials and paths
project_id = BIGQUERY_VARIABLES["project_id"]
dataset_name = BIGQUERY_VARIABLES["dataset_id"]
destination_table = BIGQUERY_VARIABLES["table_id"]
json_file_path = PATHS["json_data"]
credentials_folder = PATHS["credentials_folder"]

# Get credentials path
credentials_path = get_credentials_path(credentials_folder)

# Authenticate with Google Cloud's BigQuery service
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Read the JSON data from file
with open(json_file_path) as file:
    data = json.load(file)

# Create a BigQuery client
client = bigquery.Client(project=project_id, credentials=credentials)


# Create a reference to the dataset
dataset_ref = client.dataset(dataset_name)

# Check if dataset exists, if not, create it
try:
    client.get_dataset(dataset_ref)
except NotFound:
    dataset = bigquery.Dataset(dataset_ref)
    try:
        dataset = client.create_dataset(dataset)
        print(f"Dataset {dataset.dataset_id} created.")
    except PROJECT_NOTFOUND:
        print (f"Project '{project_id}' not found or you do not have permission to access it.")
        sys.exit()
# Create a reference to the table
table_ref = dataset_ref.table(destination_table)

# Check if table exists
try:
    client.get_table(table_ref)
    print(f"Table {destination_table} already exists.")
except NotFound:
    # Configure the load job with autodetect schema option
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True

    # Load data from JSON file into BigQuery table
    job = client.load_table_from_json(
        data,
        table_ref,
        job_config=job_config,
    )


    # # Wait for the job to complete with progress bar
    # with tqdm(total=100, desc="Loading data to BigQuery") as pbar:
    #     while not job.done():
    #         pbar.update(10)  # Update progress bar by 10%
    #         job.reload()  # Refresh job status
    #         # Add any additional logic if needed

    # Check if the job was successful
    job.result()

    print(f"Loaded {job.output_rows} rows into {destination_table}")
