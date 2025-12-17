import os

from twilio.rest import Client

from civilib.service.utils import normalize_phone_number

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = "+14155238886"


def send_whatsapp(phone_number, message):
    phone_number = normalize_phone_number(phone_number)
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=f"whatsapp:{TWILIO_WHATSAPP_FROM}",
        body=message,
        to=f"whatsapp:{phone_number}",
    )
    return message.sid
