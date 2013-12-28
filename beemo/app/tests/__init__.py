from app.tests.utils import build_test_suite_from
from .participant_tests import ParticipantTestCase

test_cases = [
    ParticipantTestCase
]

def suite():
    return build_test_suite_from(test_cases)
