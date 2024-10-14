from csv import reader 
import os
from dotenv import load_dotenv
import requests
from create_training_data import create_training_data
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load enviroment variables
load_dotenv()

# This function returns a list of websites
def extract_csv_rows(file):
    csv_file = reader(file)
    file_rows = []
    for row in csv_file:
        if row:
            file_rows.append(row[0].strip())

    return file_rows

def process_webpage(webpage):
    try:
        web_request = requests.get(webpage, timeout=5)
        if web_request.status_code == 200:
            create_training_data(web_request)
            return f"Success: {webpage}"
        else:
            return f"Failed: {webpage} - Status Code: {web_request.status_code}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Connection error: {webpage} - {conn_err}"
    except requests.exceptions.RequestException as req_ex_err:
        return f"Request error: {webpage} - {req_ex_err}"

with open(os.getenv('WEBSITES_FILE_NAME', "r")) as file:
    if file:
        csv_file_webpages = extract_csv_rows(file)

        # Use threads for faster execution
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_webpage = {executor.submit(process_webpage, webpage): webpage for webpage in csv_file_webpages}

            # Collect results as they complete
            for future in as_completed(future_to_webpage):
                webpage = future_to_webpage[future]
                try:
                    result = future.result()
                    print(result)
                except Exception as e:
                    print(f"Error processing {webpage}: {e}")

