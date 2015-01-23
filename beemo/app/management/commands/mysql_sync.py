import pprint
import csv

from django.core.management.base import BaseCommand

from sync.models import Session
from sync.models import update_participants
from sync.models import update_phone_numbers
from sync.models import update_emails
from sync.models import update_calls
from sync.models import update_problems


class Command(BaseCommand):
    help = "Updates beemo's database from remote database."

    def handle(self, *args, **options):
        session = Session()
        issue_list = list()

        update_participants(session, issue_list)
        update_phone_numbers(session, issue_list)
        update_emails(issue_list)
        update_calls(session, issue_list)
        update_problems(session, issue_list)

        keys = ['participant', 'call_num', 'field', 'reason']
        with open('issues.csv', 'wb') as csvfile:
            dw = csv.DictWriter(csvfile, delimiter=',', fieldnames=keys)
            headers = {}
            for n in keys:
                headers[n] = n
            dw.writerow(headers)
            for row in issue_list:
                dw.writerow(row)

        session.close()
