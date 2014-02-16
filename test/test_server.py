from collections import namedtuple
from datetime import date, datetime
from io import BytesIO
from unittest import TestCase
from sys import version, version_info

from taco.server import TacoServer
from taco.object import TacoObject

from . import DummyBase

class TacoServerMethodTestCase(TestCase):
    def test_server_construction(self):
        ts = DummyServer()

        self.assertEqual(ts._null_result,
            {'action': 'result', 'result': None})

    def test_find_attr(self):
        ts = DummyServer()

        self.assertEqual(ts._find_attr('__name__'), 'taco.server')

        self.assertIs(ts._find_attr('zip'), zip)

        ts.ns['test_var'] = 5678

        self.assertEqual(ts._find_attr('test_var'), 5678)

        self.assertEqual(ts._find_attr('sys.version_info.minor'),
                         version_info.minor)

    def test_object_handling(self):
        ts = DummyServer()

        self.assertEqual(ts.nobject, 0)

        d = date(2000, 4, 1)
        ts.xp.write({'object': d})

        self.assertEqual(ts.nobject, 1)

        self.assertEqual(ts.get_output(),
                        '{"object": {"_Taco_Object_": 1}}')

        ts.prepare_input('{"object": {"_Taco_Object_": 1}}')
        r = ts.xp.read()

        self.assertIs(r['object'], d)

class TacoServerActionTestCase(TestCase):
    def test_call_class_method(self):
        ts = DummyServer()
        ts.import_module({
            'name': 'datetime',
            'args': ['datetime'],
        })
        self.assertEqual(ts.call_class_method({
            'class': 'datetime',
            'name': 'strptime',
            'args': ['2011-07-31', '%Y-%m-%d'],
            'kwargs': {},
        })['result'], datetime(2011, 7, 31))

    def test_call_function(self):
        ts = DummyServer()
        self.assertEqual(ts.call_function({
            'name': 'divmod',
            'args': [67, 8],
            'kwargs': {},
        })['result'], (8, 3))

    def test_call_method(self):
        ts = DummyServer()
        ts.objects[1] = datetime(2020, 2, 20)
        self.assertEqual(ts.call_method({
            'number': 1,
            'name': 'strftime',
            'args': ['%m/%d/%Y'],
            'kwargs': {},
        })['result'], '02/20/2020')

    def test_construct_object(self):
        ts = DummyServer()
        ts.import_module({
            'name': 'datetime',
            'args': ['datetime'],
        })
        self.assertEqual(ts.construct_object({
            'class': 'datetime',
            'args': [1999, 12, 31],
            'kwargs': {'second': 59},
        })['result'], datetime(1999, 12, 31, second=59))

    def test_destroy_object(self):
        ts = DummyServer()
        ts.objects[1] = [1]
        self.assertEqual(ts.destroy_object({'number': 1})['result'], None)
        self.assertNotIn(1, ts.objects)

    def test_get_attribute(self):
        ts = DummyServer()
        TT = namedtuple('TT', ['xyz'])
        ts.objects[777] = TT(888)
        self.assertEqual(ts.get_attribute({
            'number': 777,
            'name': 'xyz',
        })['result'], 888)

    def test_get_value(self):
        ts = DummyServer()
        ts.import_module({'name': 'sys', 'args': [], 'kwargs': {}})
        self.assertEqual(ts.get_value({
            'name': 'sys.version'
        })['result'], version)

    def test_import_module(self):
        ts = DummyServer()
        self.assertNotIn('datetime', ts.ns)
        ts.import_module({'name': 'datetime', 'args': []})
        self.assertIn('datetime', ts.ns)
        self.assertNotIn('date', ts.ns)
        ts.import_module({'name': 'datetime', 'args': ['date']})
        self.assertIn('date', ts.ns)

    def test_set_attribute(self):
        ts = DummyServer()
        ob = NumberObject(44)
        ts.objects[9] = ob
        ts.set_attribute({
            'number': 9,
            'name': 'number',
            'value': 55,
        })
        self.assertEqual(ob.number, 55)

    def test_set_value(self):
        ts = DummyServer()
        d = {'xxx': 'yyy'}
        ts.ns['zzz'] = d
        ts.set_value({
            'name': 'zzz.ppp',
            'value': 'qqq'
        })
        self.assertEqual(d['ppp'], 'qqq')

class DummyServer(TacoServer, DummyBase):
    def _construct_transport(self):
        self.in_ = BytesIO()
        self.out = BytesIO()

        return TacoServer._construct_transport(self, self.in_, self.out)

class NumberObject():
    def __init__(self, number):
        self.number = number
