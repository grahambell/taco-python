from unittest import TestCase

from taco import Taco
from taco.object import TacoObject


class JavaDatetimeTestCase(TestCase):
    def test_datetime(self):
        taco = Taco(lang='java')

        self.assertIsInstance(taco, Taco)

        dt = taco.construct_object('java.util.Date', 115, 3, 1)

        self.assertIsInstance(dt, TacoObject)

        self.assertEqual(dt.call_method('getYear'), 115)
        self.assertEqual(dt.call_method('getMonth'), 3)
        self.assertEqual(dt.call_method('getDate'), 1)

        df = taco.call_class_method(
            'java.text.DateFormat', 'getDateInstance',
            taco.get_class_attribute('java.text.DateFormat', 'SHORT'),
            taco.construct_object('java.util.Locale', 'en', 'US'))

        self.assertIsInstance(df, TacoObject)

        self.assertEqual(df.call_method('format', dt), '4/1/15')
