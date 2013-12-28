import mock
from django.test import TestCase

from app.models import Participant


class ParticipantTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.participant = mock.Mock(spec=Participant)


class Class(ParticipantTestCase):

    def test_should_instantiate_object_of_its_own_type(self):
        self.failUnlessEqual(type(Participant()), Participant)
