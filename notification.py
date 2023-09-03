# Download the helper library from https://www.twilio.com/docs/python/install
import logging
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

logger=logging.getLogger() 


def SendNotificationMessage(cell_number, msg_body):
    try:
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        sender_number = os.environ['TWILIO_SENDER_PHONE_NUMBER']
    except Exception as e:
        logger.error(f'ERROR: {e}, While Fetching Data From .env file')
        return False
    
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
        from_=sender_number,
        to= cell_number,
        body= msg_body
        )
        logger.info(message)
        logger.info(f"SMS Sent TO: {cell_number} With BODY: {msg_body}")
        return True
    
    except Exception as e:
        logger.error(f'ERROR: {e}, While Sending SMS')
        return False

