from twilio.rest import Client
import os


TWILIO_ACCOUNT_SID = os.environ.get("twilio_AccSID")
TWILIO_AUTH_TOKEN = os.environ.get("twilio_AuthToken")

from_number = os.environ.get("from_num")
to_number = os.environ.get("to_num")

class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def print_message(self, message):
        message = self.client.messages.create(
            body=message,
            from_=from_number,
            to=to_number)
        print(message.status)
