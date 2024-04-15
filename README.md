# Automate-BigQuery-Sandbox-Uploading-Data-and-Load-Credentials-into-Streamlit's-secrets.toml

This repository was prepared to automate loading data to BigQuery and Bigquery sandbox, and generating `secrets.toml` for experimental and educational purposes. All you need is to get your JSON credentials and add them to the `credentials_folder`.

# credentials.py

This script has the ability to convert BigQuery JSON credentials to TOML format.

## Prerequisites:

* Ensure that the path `.streamlit/secrets.toml` exists.
* Ensure that only one JSON credentials file is located in the `credentials_folder` by default.
* These default settings can be changed by modifying variables located in `config.py`.

# load_json_data_to_bigquery.py

This script uploads JSON data, even with nested structures, to BigQuery.

> It works with BigQuery sandbox with free tier limitations.

## Prerequisites:

* Ensure that only one JSON credentials file is located in the `credentials_folder` by default.
* Ensure that the `project_id`, `dataset_id`, and `table_id` are defined in `config.py`.
