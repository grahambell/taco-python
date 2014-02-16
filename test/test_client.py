from io import BytesIO
from unittest import TestCase

from taco import Taco
from taco.object import TacoObject

from . import DummyBase

# This assert method was renamed in Python 3.2.
if not hasattr(TestCase, 'assertRaisesRegex'):
    TestCase.assertRaisesRegex = TestCase.assertRaisesRegexp

class TacoClientMethodTestCase(TestCase):
    def test_interaction(self):
        t = DummyClient()

        t.prepare_input('{"action": "result", "result": 46}')

        self.assertEqual(t._interact({'action': 'test'}), 46)
        self.assertEqual(t.get_output(), '{"action": "test"}')

        t.prepare_input('{"action": "non-existent action"}')

        with self.assertRaisesRegex(Exception, 'received unknown action'):
            t._interact({'action': 'test'})

        t.prepare_input('{"action": "exception", "message": "test_exc"}')

        with self.assertRaisesRegex(Exception, 'test_exc'):
            t._interact({'action': 'test'})

    def test_object_handing(self):
        t = DummyClient()

        t.prepare_input('{"action": "result", "result": null}')
        o = TacoObject(t, 345)
        t._interact({'test_object': o})
        self.assertEqual(t.get_output(),
            '{"test_object": {"_Taco_Object_": 345}}')

        t.prepare_input('{"action": "result", "result": {"_Taco_Object_": 78}}')
        r = t._interact({'action': 'test'})

        self.assertIsInstance(r, TacoObject)
        self.assertEqual(r.number, 78)

class DummyClient(Taco, DummyBase):
    def __init__(self):
        self.disable_context = False
        self.in_ = BytesIO()
        self.out = BytesIO()

        self.xp = self._construct_transport(self.in_, self.out)

    def _destroy_object(self, number):
        pass
