from unittest import TestCase
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from taco.object import TacoObject

class TacoObjectTestCase(TestCase):
    def test_create_destroy(self):
        client = Mock()

        obj = TacoObject(client, 77)

        self.assertIsInstance(obj, TacoObject)

        del obj

        client._destroy_object.assert_called_with(77)

    def test_methods(self):
        client = Mock()

        obj = TacoObject(client, 84)

        obj.call_method('test_method', 1, 2, three=3, four=4)
        client._call_method.assert_called_with(
            84, 'test_method', 1, 2, three=3, four=4)

        obj.set_attribute('test_attribute', 4444)
        client._set_attribute.assert_called_with(
            84, 'test_attribute', 4444)

        g_a = Mock(return_value=55555)
        client._get_attribute = g_a
        self.assertEqual(obj.get_attribute('test_attribute2'), 55555)
        g_a.assert_called_with(84, 'test_attribute2')

    def test_convenience(self):
        client = Mock()

        obj = TacoObject(client, 333)

        conv = obj.method('conv')

        conv(5, 6, 7, 8)

        client._call_method.assert_called_with(333, 'conv', 5, 6, 7, 8)
