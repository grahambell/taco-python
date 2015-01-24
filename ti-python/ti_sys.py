from unittest import TestCase

from taco import Taco
from taco.object import TacoObject

class PythonSysTestCase(TestCase):
    def test_sys(self):
        taco = Taco(script='scripts/taco-python')

        taco.import_module('sys')

        # Non-interactive, so sys.ps1 should not be set initially.
        with self.assertRaises(Exception):
            taco.get_value('sys.ps1')

        taco.set_value('sys.ps1', '!!! ')

        self.assertEqual(taco.get_value('sys.ps1'), '!!! ')

        # First element of sys.version_info 2 or 3?
        r = taco.get_value('sys.version_info')
        if isinstance(r, TacoObject):
            r = taco.construct_object('list', r)

        self.assertIsInstance(r, list)

        self.assertIn(r[0], (2, 3))
