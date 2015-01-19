import mock

from django.test import TestCase

from app.models import InterventionParticipant


class InterventionParticipantTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.participant = mock.Mock(spec=InterventionParticipant)

        cls.emails_in = 1
        cls.calls_in = 3
        cls.sms_in = 5

        cls.emails_out = 7
        cls.calls_out = 9
        cls.sms_out = 11


class Class(InterventionParticipantTestCase):

    def test_should_instantiate_object_of_its_own_type(self):
        self.failUnlessEqual(
            type(InterventionParticipant()), InterventionParticipant)


class TechnologyTouchesProperties(InterventionParticipantTestCase):

    def test_should_sum_inbound_values_properly(self):
        self.assertEqual(
            self.participant.tt_in, self.participant.emails_in +
            self.participant.calls_in + self.participant.sms_in)

    def test_should_sum_outbound_values_properly(self):
        self.assertEqual(
            self.participant.tt_out, self.participant.emails_out +
            self.participant.calls_out + self.participant.sms_out)

    def test_should_sum_all_values_properly(self):
        self.assertEqual(self.participant.technology_touches,
                         self.participant.tt_in + self.participant.tt_out)
