import requests
from django.conf import settings


def send_sms(phone_number, message):
    url = "https://notify.eskiz.uz/api/message/sms/send"
    headers = {"Authorization": f"Bearer {settings.ESKIZ_API_TOKEN}"}
    data = {
        "mobile_phone": phone_number,
        "message": message,
        "from": "4546",
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
