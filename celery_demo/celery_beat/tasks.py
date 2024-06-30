# import os
#
# import requests
# from celery import shared_task
# from django.core.cache import cache

import os
import requests
import json
from celery import shared_task
from django.conf import settings

API_URL = "http://localhost:8000/core/api-call/"


# @shared_task
# def fetch_and_cache_data():
#     response = requests.get(API_URL)
#     if response.status_code != 200:
#         raise Exception(f"API request failed with status code {response.status_code}")
#     data = response.json()
#
#     cache.set("products_data", data)
#     return data

@shared_task
def fetch_and_cache_data():
    response = requests.get(API_URL)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")

    data = response.json()

    # Define the directory where you want to store the files
    storage_directory = os.path.join(settings.BASE_DIR, 'mediafiles', 'data_storage_directory')

    # # Ensure the directory exists; create it if it doesn't
    # if not os.path.exists(storage_directory):
    #     os.makedirs("data_storage_directory")

    # Generate a unique filename (you can customize the naming scheme)
    filename = os.path.join(storage_directory, 'api_data.json')

    # Write the data to the file
    with open(filename, 'w') as f:
        json.dump(data, f)

    return filename

