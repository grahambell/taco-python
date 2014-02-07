from unittest import TestCase

from taco import Taco
from taco.object import TacoObject

class TacoClientActionTestCase(TestCase):
    def test_call_class_method(self):
        t = DummyClient()
        t.call_class_method('tc', 'tm', 1, 2, 3, four=4, five=5)
        self.assertEqual(t.msg, {
            'action': 'call_class_method',
            'class': 'tc',
            'name': 'tm',
            'args': (1, 2, 3),
            'kwargs': {'four': 4, 'five': 5},
            'context': None,
        })

    def test_call_function(self):
        t = DummyClient()
        t.call_function('tf', 1, 2, 3, four=4, five=5)
        self.assertEqual(t.msg, {
            'action': 'call_function',
            'name': 'tf',
            'args': (1, 2, 3),
            'kwargs': {'four': 4, 'five': 5},
            'context': None,
        })

    def test_call_method(self):
        t = DummyClient()
        o = TacoObject(t, 4444)
        o.call_method('tm', 1, 2, 3, four=4, five=5)
        self.assertEqual(t.msg, {
            'action': 'call_method',
            'number': 4444,
            'name': 'tm',
            'args': (1, 2, 3),
            'kwargs': {'four': 4, 'five': 5},
            'context': None,
        })

    def test_construct_object(self):
        t = DummyClient()
        t.construct_object('tc', 5, 6, 7, 8, x=111, y=222)
        self.assertEqual(t.msg, {
            'action': 'construct_object',
            'class': 'tc',
            'args': (5, 6, 7, 8),
            'kwargs': {'x': 111, 'y': 222},
        })

    def test_destroy_object(self):
        t = DummyClient()
        o = TacoObject(t, 55555)
        del o
        self.assertEqual(t.msg, {
            'action': 'destroy_object',
            'number': 55555,
        })

    def test_get_attribute(self):
        t = DummyClient()
        o = TacoObject(t, 666666)
        o.get_attribute('ta')
        self.assertEqual(t.msg, {
            'action': 'get_attribute',
            'number': 666666,
            'name': 'ta',
        })

    def test_get_value(self):
        t = DummyClient()
        t.get_value('tv')
        self.assertEqual(t.msg, {
            'action': 'get_value',
            'name': 'tv',
        })

    def test_import_module(self):
        t = DummyClient()
        t.import_module('module.name')
        self.assertEqual(t.msg, {
            'action': 'import_module',
            'name': 'module.name',
            'args': (),
            'kwargs': {},
        })

    def test_set_attrbute(self):
        t = DummyClient()
        o = TacoObject(t, 7777777)
        o.set_attribute('ta', 88)
        self.assertEqual(t.msg, {
            'action': 'set_attribute',
            'number': 7777777,
            'name': 'ta',
            'value': 88,
        })

    def test_set_value(self):
        t = DummyClient()
        t.set_value('value.name', 999)
        self.assertEqual(t.msg, {
            'action': 'set_value',
            'name': 'value.name',
            'value': 999,
        })

class TacoClientConvenienceTestCase(TestCase):
    def test_function(self):
        t = DummyClient()
        f = t.function('convfunc')
        f('arg1', 'arg2', kwarg1=9, kwarg2=99)
        self.assertEqual(t.msg, {
            'action': 'call_function',
            'name': 'convfunc',
            'args': ('arg1', 'arg2'),
            'kwargs': {'kwarg1': 9, 'kwarg2': 99},
            'context': None,
        })

    def test_constructor(self):
        t = DummyClient()
        c = t.constructor('convclass')
        c(3, 3, 3, x=1, y=2)
        self.assertEqual(t.msg, {
            'action': 'construct_object',
            'class': 'convclass',
            'args': (3, 3, 3),
            'kwargs': {'x': 1, 'y': 2},
        })

class DummyClient(Taco):
    def __init__(self):
        self.msg = None

    def _interact(self, msg):
        self.msg = msg
