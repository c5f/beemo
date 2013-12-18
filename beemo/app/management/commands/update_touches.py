import requests
from imapclient import IMAPClient

from django.core.management.base import BaseCommand

from beemo.settings import GMAIL_INFO, TWILIO_INFO
from app.models import Participant

twilio_base_url = 'https://api.twilio.com/2010-04-01/Accounts/%s/' % TWILIO_ACCOUNT_SID
twilio_auth = (TWILIO_INFO['sid'], TWILIO_INFO['token'])


def update_email_counts(participant):
    gmail = IMAPClient(
        'imap.gmail.com',
        use_uid=True,
        ssl=True
    )

    gmail.login(GMAIL_INFO['user'], GMAIL_INFO['pass'])


def update_call_counts(participant):
    
    calls_url = twilio_base_url + 'Calls.json'
    calls_in = 0
    calls_out = 0

    for phone in participant.phone_numbers.all():
        
        phone_number = '+1' + phone.number
        response = requests.get(
            calls_url,
            auth=twilio_auth,
            params={'To': phone_number, 'PageSize': 1}
        ).json()

        calls_in += response['total']

        response = requests.get(
            calls_url,
            auth=twilio_auth,
            params={'From': phone_number, 'PageSize': 1}
        ).json()

        calls_out += response['total']

    participant.calls_in = calls_in
    participant.calls_out = calls_out
    participant.save()


def update_sms_counts(participant):

    sms_number = '+1' + participant.sms_number.number
    messages_url = twilio_base_url + 'Messages.json'
    
    response = requests.get(
        messages_url,
        auth=twilio_auth,
        params={'To': sms_number}
    ).json()

    participant.sms_in = response['total']

    payload = {'From': sms_number}
    response = requests.get(
        messages_url,
        auth=twilio_auth,
        params={'From': sms_number}
    ).json()

    participant.sms_out = response['total']

    participant.save()


def update_technology_touches():

    for participant in Participant.objects.all():
        
        update_email_counts(participant)
        update_call_counts(participant)

        if participant.sms_number:
            update_sms_counts(participant)


class Command(BaseCommand):
    help = "Updates technology touch counts using IMAPClient and Twilio's REST API."

    def handle(self, *args, **options):

        update_technology_touches()
