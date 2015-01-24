import requests
from imapclient import IMAPClient

from django.core.management.base import BaseCommand

from beemo.settings import GMAIL_ACCTS
from beemo.settings import TWILIO_INFO

from app.models import InterventionParticipant

twilio_base_url = 'https://api.twilio.com/2010-04-01/Accounts/%s/' %\
    TWILIO_INFO['sid']
twilio_auth = (TWILIO_INFO['sid'], TWILIO_INFO['token'])


def update_email_counts(participant, server):

    emails_in = 0
    emails_out = 0

    for email in participant.emails.all():
        messages = server.search('FROM %s' % email.email)
        emails_out += len(messages)

        messages = server.search('TO %s' % email.email)
        emails_in += len(messages)

    participant.emails_in = emails_in
    participant.emails_out = emails_out
    participant.save()


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

    sms_in = response['total']

    payload = {'From': sms_number}
    response = requests.get(
        messages_url,
        auth=twilio_auth,
        params={'From': sms_number}
    ).json()

    sms_out = response['total']

    participant.sms_in = sms_in
    participant.sms_out = sms_out
    participant.save()


def update_technology_touches():

    update_control_technology_touches()
    update_intervention_technology_touches()


def update_control_technology_touches():

    gmail = IMAPClient(
        'imap.gmail.com',
        use_uid=True,
        ssl=True
    )

    gmail.login(*GMAIL_ACCTS['control'])
    gmail.select_folder('[Gmail]/All Mail')

    for participant in ControlParticipant.objects.all():

        update_email_counts(participant, gmail)
        update_call_counts(participant)

        if participant.sms_number:
            update_sms_counts(participant)

    gmail.logout()


def update_intervention_technology_touches():

    gmail = IMAPClient(
        'imap.gmail.com',
        use_uid=True,
        ssl=True
    )

    gmail.login(*GMAIL_ACCTS['intervention'])
    gmail.select_folder('[Gmail]/All Mail')

    for participant in InterventionParticipant.objects.all():

        update_email_counts(participant, gmail)
        update_call_counts(participant)

        if participant.sms_number:
            update_sms_counts(participant)

    gmail.logout()


class Command(BaseCommand):
    help = "Updates technology touch counts using IMAPClient and Twilio's \
        REST API."

    def handle(self, *args, **options):

        update_technology_touches()
