import requests
from celery import shared_task
from django.conf import settings


@shared_task
def send_get_request():
    url = f"{settings.RENDER_BACKEND_URL}/api/tasks/"  # Adjust the URL as needed
    try:
        response = requests.get(url)
        print(f"Request to {url} successful: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request to {url} failed: {str(e)}")
