from unittest import TestCase

from taco import Taco
from taco.object import TacoObject

class PythonDatetimeTestCase(TestCase):
    def test_datetime(self):
        taco = Taco(script='scripts/taco-python')

        taco.import_module('datetime')

        dt = taco.construct_object('datetime.datetime', 2000, 12, 25)

        self.assertIsInstance(dt, TacoObject)
        self.assertEqual(
            dt.get_attribute('__class__').get_attribute('__name__'),
            'datetime')

        self.assertEqual(dt.get_attribute('year'), 2000)
        self.assertEqual(dt.get_attribute('month'), 12)
        self.assertEqual(dt.get_attribute('day'), 25)

        self.assertEqual(
            dt.call_method('strftime', '%Y-%m-%d'),
            '2000-12-25')

        dt_d = dt.call_method('date')

        self.assertIsInstance(dt_d, TacoObject)
        self.assertEqual(
            dt_d.get_attribute('__class__').get_attribute('__name__'),
            'date')

        dt_t = taco.construct_object('datetime.time', 15, 0)

        self.assertIsInstance(dt_t, TacoObject)
        self.assertEqual(
            dt_t.get_attribute('__class__').get_attribute('__name__'),
            'time')

        self.assertEqual(dt_t.get_attribute('hour'), 15)
        self.assertEqual(dt_t.get_attribute('minute'), 0)

        dt_c = taco.call_class_method('datetime.datetime', 'combine',
            dt_d, dt_t)

        self.assertIsInstance(dt_c, TacoObject)
        self.assertEqual(
            dt_c.get_attribute('__class__').get_attribute('__name__'),
            'datetime')

        dt_c2 = dt_c.call_method('replace', year=2010)

        self.assertIsInstance(dt_c2, TacoObject)

        self.assertEqual(
            dt_c2.call_method('strftime', '%d/%m/%Y %I:%M %p'),
            '25/12/2010 03:00 PM')

        self.assertRegex(
            taco.call_function('repr', dt_c2),
            '^datetime\.datetime\(2010')
