from app.tests.utils import build_test_suite_from
from .participant_tests import ParticipantTestCase
from .model_util_tests import ModelUtilTestCase

test_cases = [
    ParticipantTestCase,
    ModelUtilTestCase
]

def suite():
    return build_test_suite_from(test_cases)
