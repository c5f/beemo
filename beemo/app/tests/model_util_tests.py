import mock

from django.test import TestCase

from app.models import Participant
from app.models import Call
from app.models import calculate_adherence_score
from app.models import calculate_veg_servings_score
from app.models import calculate_fruit_servings_score
from app.models import calculate_fiber_grams_score
from app.models import calculate_fat_grams_score
from app.models import calculate_steps_score


class ModelUtilTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.participant = mock.Mock(spec=Participant)
        cls.call = mock.Mock(spec=Call)

        cls.participant.base_fat_goal = None
        cls.participant.base_step_goal = None
        cls.call.fat_grams = None
        cls.call.fiber_grams = None
        cls.call.fruit_servings = None
        cls.call.veg_servings = None
        cls.call.steps = None


class AdherenceScoreTestCase(ModelUtilTestCase):

    def test_should_return_not_none_when_all_values_present(self):
        self.participant.base_fat_goal = 1
        self.participant.base_step_goal = 1
        self.call.fat_grams = 1
        self.call.fiber_grams = 1
        self.call.fruit_servings = 1
        self.call.veg_servings = 1
        self.call.steps = 1

        self.assertIsNotNone(
            calculate_adherence_score(self.participant, self.call))

    def test_should_return_none_when_single_value_missing(self):
        self.participant.base_fat_goal = 1
        self.participant.base_step_goal = 1
        self.call.fat_grams = 1
        self.call.fiber_grams = 1
        self.call.fruit_servings = 1
        self.call.veg_servings = 1
        self.call.steps = None

        self.assertIsNone(
            calculate_adherence_score(self.participant, self.call))

        self.call.steps = 1
        self.call.veg_servings = None
        self.assertIsNone(
            calculate_adherence_score(self.participant, self.call))

        self.call.veg_servings = 1
        self.call.fruit_servings = None
        self.assertIsNone(
            calculate_adherence_score(self.participant, self.call))

        self.call.fruit_servings = 1
        self.call.fiber_grams = None
        self.assertIsNone(
            calculate_adherence_score(self.participant, self.call))

        self.call.fiber_grams = 1
        self.participant.base_step_goal = None
        self.assertIsNone(
            calculate_adherence_score(self.participant, self.call))

        self.participant.base_step_goal = 1
        self.participant.base_fat_goal = None
        self.assertIsNone(
            calculate_adherence_score(self.participant, self.call))

    def test_should_return_none_when_multiple_values_missing(self):
        self.assertIsNone(
            calculate_adherence_score(self.participant, self.call))

    def test_should_calculate_correct_veg_scores(self):
        for value in range(1, 10):
            if value < 2:
                self.assertEqual(calculate_veg_servings_score(value), 0,
                                 'wrong veg score for value %s' % value)
            elif value < 3:
                self.assertEqual(calculate_veg_servings_score(value), 1,
                                 'wrong veg score for value %s' % value)
            elif value < 4:
                self.assertEqual(calculate_veg_servings_score(value), 3,
                                 'wrong veg score for value %s' % value)
            elif value >= 4:
                self.assertEqual(calculate_veg_servings_score(value), 5,
                                 'wrong veg score for value %s' % value)

    def test_should_calculate_correct_fruit_scores(self):
        for value in range(1, 10):
            if value < 1:
                self.assertEqual(calculate_fruit_servings_score(value), 0,
                                 'wrong fruit score for value %s' % value)
            elif value < 2:
                self.assertEqual(calculate_fruit_servings_score(value), 1,
                                 'wrong fruit score for value %s' % value)
            elif value < 3:
                self.assertEqual(calculate_fruit_servings_score(value), 3,
                                 'wrong fruit score for value %s' % value)
            else:
                self.assertEqual(calculate_fruit_servings_score(value), 5,
                                 'wrong fruit score for value %s' % value)

    def test_should_calculate_correct_fiber_scores(self):
        for value in range(1, 50):
            if value < 15:
                self.assertEqual(calculate_fiber_grams_score(value), 0,
                                 'wrong fiber score for value %s' % value)
            elif value < 20:
                self.assertEqual(calculate_fiber_grams_score(value), 1,
                                 'wrong fiber score for value %s' % value)
            elif value < 30:
                self.assertEqual(calculate_fiber_grams_score(value), 3,
                                 'wrong fiber score for value %s' % value)
            else:
                self.assertEqual(calculate_fiber_grams_score(value), 5,
                                 'wrong fiber score for value %s' % value)

    def test_should_calculate_correct_fat_scores(self):
        base_value = 30

        for value in range(1, 50):
            percentage = value / float(base_value)

            if percentage >= 1.4:
                self.assertEqual(
                    calculate_fat_grams_score(value, base_value), 0,
                    'wrong fat score value for value %s and base value %s' %
                    (value, base_value))
            elif percentage >= 1.2:
                self.assertEqual(
                    calculate_fat_grams_score(value, base_value), 1,
                    'wrong fat score value for value %s and base value %s' %
                    (value, base_value))
            elif percentage >= 1.1:
                self.assertEqual(
                    calculate_fat_grams_score(value, base_value), 3,
                    'wrong fat score value for value %s and base value %s' %
                    (value, base_value))
            else:
                self.assertEqual(
                    calculate_fat_grams_score(value, base_value), 5,
                    'wrong fat score value for value %s and base value %s' %
                    (value, base_value))

    def test_should_calculate_correct_step_scores(self):
        base_value = 4000

        for value in range(0, 10):
            difference = value * 500 - base_value

            if difference > 2000:
                self.assertEqual(
                    calculate_steps_score(value * 500, base_value), 0,
                    'wrong step score value for value %s and base value %s' %
                    (value * 500, base_value))
            elif difference > 1000:
                self.assertEqual(
                    calculate_steps_score(value * 500, base_value), 1,
                    'wrong step score value for value %s and base value %s' %
                    (value * 500, base_value))
            elif difference > 1:
                self.assertEqual(
                    calculate_steps_score(value * 500, base_value), 3,
                    'wrong step score value for value %s and base value %s' %
                    (value * 500, base_value))
            else:
                self.assertEqual(
                    calculate_steps_score(value * 500, base_value), 5,
                    'wrong step score value for value %s and base value %s' %
                    (value * 500, base_value))

    def test_should_calculate_correct_adherence_score(self):
        pass
