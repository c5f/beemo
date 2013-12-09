import datetime, locale
locale.setlocale(locale.LC_ALL, 'en_us')

from django.core.management.base import BaseCommand

from app.models import Email, Phone, Participant, Call, ParticipantProblem

from sync.models import Session, RNode, RParticipant, RCall, RPhone, RProblem


def update_participants(session, issue_list):

    for r_participant in session.query(RParticipant).filter_by(ptype=1):

        mobile = None

        if r_participant.mobile:
            mobile = Phone.objects.get_or_create(number=r_participant.mobile)[0]

        r_node = session.query(RNode).get(r_participant.nid)

        try:
            participant = Participant.objects.get(pid=r_participant.pid)
        except Participant.DoesNotExist:
            participant = Participant(pid=r_participant.pid)

        participant.creation_date = datetime.datetime.fromtimestamp(r_node.created)
        participant.sms_number = mobile

        try:
            participant.base_fat_goal = locale.atoi(r_participant.fat_grams)
        except AttributeError:
            participant.base_fat_goal = None
        except ValueError:
            issue_list.append({
                'participant_id': participant.pid,
                'issue': 'ValueError',
                'field': 'base_fat_goal',
                'value': r_participant.fat_grams
            })

            participant.base_fat_goal = None

        try:
            participant.base_step_goal = locale.atoi(r_participant.steps)
        except AttributeError:
            participant.base_step_goal = None
        except ValueError:
            issue_list.append({
                'participant_id': participant.pid,
                'issue': 'ValueError',
                'field': 'base_step_goal',
                'value': r_participant.steps
            })

            participant.base_step_goal = None

        if mobile:
            participant.phone_numbers.add(mobile)

        participant.save()

        if r_participant.email:
            email = Email.objects.get_or_create(email=r_participant.email, participant=participant)[0]


def update_phone_numbers(session, issue_list):

    for r_phone in session.query(RPhone).all():

        # Check if this phone belongs to a Participant that beemo is tracking
        pid = session.query(RParticipant.pid).filter_by(nid=r_phone.nid).first()[0]
        try:
            participant = Participant.objects.get(pid=pid)

            # Strip non-digit characters
            phone_number = ''.join([i for i in r_phone.phone if i.isdigit()])

            # Trim anything beyond 10 digits
            phone_number = phone_number[:10]

            # Add this phone number to our database
            phone = Phone.objects.get_or_create(number=phone_number)

            # Add this phone number to this participant
            participant.phone_numbers.add(phone)

        except Participant.DoesNotExist:
            # Beemo is not tracking this Participant
            pass


def update_emails(issue_list):

    # Add emails from flat file to corresponding participants
    pass


def update_calls(session, issue_list):

    pass


def update_problems(session, issue_list):

    pass


class Command(BaseCommand):
    help = "Updates beemo's database from remote database."

    def handle(self, *args, **options):

        # Clear existing records


        session = Session()
        issue_list = list()

        update_participants(session, issue_list)
        update_phone_numbers(session, issue_list)
        update_emails(issue_list)
        update_calls(session, issue_list)
        update_problems(session, issue_list)

        print issue_list
        session.close()

if __name__ == '__main__':
    session = Session()
    issue_list = list()

    update_participants(session, issue_list)
    update_phone_numbers(session, issue_list)
    update_emails(issue_list)
    update_calls(session, issue_list)
    update_problems(session, issue_list)

    print issue_list
    session.close()