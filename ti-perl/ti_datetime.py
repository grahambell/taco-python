from unittest import TestCase

from taco import Taco
from taco.object import TacoObject

# These assert methods were added / renamed in Python 3.2.
if not hasattr(TestCase, 'assertNotRegex'):
    def assertNotRegex(self, *args):
        try:
            self.assertRegexpMatches(*args)
        except AssertionError:
            pass
        else:
            raise AssertionError('assertNotRegex found match')

    TestCase.assertRegex = TestCase.assertRegexpMatches
    TestCase.assertNotRegex = assertNotRegex

class PerlDatetimeTestCase(TestCase):
    def test_datetime(self):
        taco = Taco(lang='perl')

        taco.import_module('DateTime')

        dt = taco.construct_object('DateTime',
            year=2000, month=4, day=1)

        self.assertIsInstance(dt, TacoObject)

        self.assertEqual(dt.call_method('ymd', '/'), '2000/04/01')

        strftime = dt.method('strftime')

        self.assertEqual(strftime('%d-%m-%Y'), '01-04-2000')

        taco.import_module('Data::Dumper')
        dumper = taco.function('Dumper')

        self.assertNotRegex(dumper(dt), '_taco_test_attr')
        dt.set_attribute('_taco_test_attr', 12345)
        self.assertRegex(dumper(dt), '_taco_test_attr')
        self.assertEqual(dt.get_attribute('_taco_test_attr'), 12345)

        taco.import_module('DateTime::Duration')
        Duration = taco.constructor('DateTime::Duration')
        dur = Duration(days=3)

        self.assertIsInstance(dur, TacoObject)

        taco.import_module('Storable', 'dclone')
        dt_orig = taco.call_function('dclone', dt)

        self.assertIsInstance(dt_orig, TacoObject)

        dt.call_method('add_duration', dur)

        self.assertEqual(strftime('%d-%m-%Y'), '04-04-2000')

        dur_diff = dt_orig.call_method('delta_days', dt)

        self.assertEqual(dur_diff.call_method('days'), 3)

        dt2 = taco.call_class_method('DateTime', 'from_epoch',  epoch=15)

        self.assertEqual(dt2.call_method('datetime'), '1970-01-01T00:00:15')
