import logging

import requests
from celery import shared_task
from django.core.cache import cache

API_URL = "http://polls-app:8000/core/api-call/"
logger = logging.getLogger(__name__)


@shared_task
def fetch_and_cache_data():
    try:
        response = requests.get(API_URL, headers={'Accept': 'application/json'})
        logger.info(response)
        if response.status_code == 200:
            data = response.json()

            # TODO make mechanism to compare already cached data with new one and update only if needed.

            cache.set('api_data', data, timeout=60*60)  # Cache data for 1 hour
            return "Data fetched and cached successfully"
        else:
            return f"Failed to fetch data: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

