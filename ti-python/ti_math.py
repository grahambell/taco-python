import math
from unittest import TestCase

from taco import Taco

class PythonMathTestCase(TestCase):
    def test_math(self):
        taco = Taco(script='scripts/taco-python')

        taco.import_module('math')

        self.assertAlmostEqual(
            taco.call_function('math.sin', math.pi),
            0.0)
