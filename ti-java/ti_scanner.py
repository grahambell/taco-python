from unittest import TestCase

from taco import Taco
from taco.object import TacoObject


class JavaScannerTestCase(TestCase):
    def test_scanner(self):
        taco = Taco(lang='java')

        self.assertIsInstance(taco, Taco)

        sb = taco.construct_object('java.lang.StringBuilder')

        self.assertIsInstance(sb, TacoObject)

        append = sb.method('append')
        append('1 1 2 ')
        append('3 5 8')

        seq = sb.call_method('toString')

        self.assertEqual(seq, '1 1 2 3 5 8')

        sc = taco.construct_object(
            'java.util.Scanner',
            taco.construct_object('java.io.StringReader', seq))

        self.assertIsInstance(sc, TacoObject)

        nxt = sc.method('nextInt')

        self.assertEqual(nxt(), 1)
        self.assertEqual(nxt(), 1)
        self.assertEqual(nxt(), 2)
        self.assertEqual(nxt(), 3)
        self.assertEqual(nxt(), 5)
        self.assertEqual(nxt(), 8)
