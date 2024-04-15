import os
import json
from config import PATHS

def get_credentials_path(credentials_dir:str):
    json_files = [file for file in os.listdir(credentials_dir) if file.endswith('.json')]
    
    if len(json_files) == 0:
        raise FileNotFoundError(f"No JSON files found in directory: {credentials_dir}")
    elif len(json_files) > 1:
        raise InterruptedError(f"More than one JSON file has been found. Please ensure there is only one JSON file located in the directory: {credentials_dir}.\nJSONs found:\n{', '.join(json_files)}")

    credential_file = json_files[0]
    return os.path.join(credentials_dir, credential_file)

def load_credentials(credentials_dir:str):
    """Load credentials from JSON file."""
    credential_file_path = get_credentials_path(credentials_dir=credentials_dir)
    print(f"Found credentials file: {credential_file_path}")

    return json.load(open(credential_file_path))


def convert_to_toml(credentials_dict, toml_file_path):
    """Convert credentials dictionary to TOML format and save to file."""
    if not os.path.exists(toml_file_path):
        raise FileNotFoundError(f"{toml_file_path} not found.")
    toml_string = "[gcp_service_account]"
    for key, value in credentials_dict.items():
        if key != 'universe_domain':
            toml_string += "\n" + ('sttype' if key == 'type' else key) + " = \"" + value.replace('\n', '\\n') + "\""


    with open(toml_file_path, 'w') as file:
        file.truncate()
        file.write(toml_string)
        print(f"Credentials converted and saved to: {toml_file_path}")


if __name__ == "__main__":
    credentials_dir = PATHS["credentials_folder"]
    secret_file_path = PATHS["secrets"]

    print("Loading credentials...")
    try:
        credentials_dict = load_credentials(credentials_dir)
        print("Credentials loaded successfully.")

        print("Converting credentials to TOML format...")
        convert_to_toml(credentials_dict, secret_file_path)
        print("Conversion and laoding completed.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except InterruptedError as e:
        print(f"Error: {e}")


