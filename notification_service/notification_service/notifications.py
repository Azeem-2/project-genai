# notification.py
import smtplib
from twilio.rest import Client
from notification_service.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
import logging
from notification_service.settings import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email_notification(to_email: str, subject: str, message: str):
    smtp_server = str(SMTP_SERVER)
    smtp_port = int(SMTP_PORT)
    smtp_username = str(SMTP_USERNAME)
    smtp_password = str(SMTP_PASSWORD)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.set_debuglevel(1)  # Enable debug output for detailed logs
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_username, smtp_password)
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(smtp_username, to_email, email_message)
        logger.info(f"Email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")

def send_sms_notification(to_phone: str, message: str):
    account_sid = str(TWILIO_ACCOUNT_SID)  # Convert Secret to string
    auth_token = str(TWILIO_AUTH_TOKEN)  # Convert Secret to string
    client = Client(account_sid, auth_token)
    
    from_phone = str(TWILIO_PHONE_NUMBER)  # Convert Secret to string
    try:
        response = client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
        logger.info(f"SMS sent to {to_phone}, SID: {response.sid}, Status: {response.status}, Response: {response}")
    except Exception as e:
        logger.error(f"Failed to send SMS to {to_phone}: {e}")
    