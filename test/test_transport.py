from codecs import utf_8_decode, utf_8_encode
from io import BytesIO
from unittest import TestCase

from taco.transport import TacoTransport

class TacoTransportTestCase(TestCase):
    def test_transport(self):
        in_ = BytesIO(utf_8_encode('{"test_input":1}\n// END\n')[0])
        out = BytesIO()

        xp = TacoTransport(in_, out)

        xp.write({'test_output': 2})

        r = utf_8_decode(out.getvalue())[0]

        self.assertEqual(r, "{\"test_output\": 2}\n// END\n")

        r = xp.read()

        self.assertEqual(r, {'test_input': 1})
