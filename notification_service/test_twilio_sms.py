# test_twilio_sms.py
import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
to_phone_number = "+14158147533"  # Replace with a valid phone number
message_body = "Test message from Twilio"

client = Client(account_sid, auth_token)

try:
    response = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=to_phone_number
    )
    print(f"SMS sent to {to_phone_number}, SID: {response.sid}, Status: {response.status}, Response: {response}")
except Exception as e:
    print(f"Failed to send SMS: {e}")
