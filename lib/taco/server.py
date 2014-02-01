# Taco Python server module.
# Copyright (C) 2013-2014 Graham Bell
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

import sys

from taco.transport import TacoTransport

actions = [
    'call_class_method',
    'call_function',
    'call_method',
    'construct_object',
    'destroy_object',
    'get_attribute',
    'get_value',
    'import_module',
    'set_attribute',
    'set_value',
]

def main():
    """Main server function.

    Constructs a TacoTransport object communicating via standard
    input and standard output, and then enters a message handling
    loop.  The loop exits on failure to read another message.

    sys.stdout is set to sys.stderr to try to avoid text being
    written to standard output, which would corrupt communications
    with the client.
    """

    # When running under Python 3, detach the text wrappers from
    # stdin and stdout so that we have binary streams which act
    # like other streams which TacoTransport needs to handle.
    try:
        in_ = sys.stdin.detach()
        out = sys.stdout.detach()
    except AttributeError:
        in_ = sys.stdin
        out = sys.stdout

    # Redirect stdout to stderr to prevent any called functions from
    # writing into the Taco message stream.
    sys.stdout = sys.stderr

    xp = TacoTransport(in_, out, _from_obj, _to_obj)

    while True:
        message = xp.read()

        if message is None:
            break

        act = message['action']

        if act in actions:
            try:
                res = globals()[act](message)
            except Exception as e:
                res = {
                    'action': 'exception',
                    'message': 'exception caught: ' + str(e),
                }
        else:
            res = {
                'action': 'exception',
                'message': 'unknown action: ' + act,
            }

        xp.write(res)

ns = {}
objects = {}
nobject = 0

def _from_obj(obj):
    """Place object in the objects dictionary and return a Taco object
    reference."""

    global nobject
    nobject += 1
    objects[nobject] = obj
    return {'_Taco_Object_': nobject}

def _to_obj(dict_):
    """If dict_ is a Taco object reference, fetch the corresponding
    object from objects dictionary."""

    if '_Taco_Object_' in dict_:
        return objects[dict_['_Taco_Object_']]
    else:
        return dict_

def _make_result(result):
    """Construct Taco result message."""

    return {
        'action': 'result',
        'result': result,
    }

null_result = _make_result(None)

def _find_attr(name):
    """Attempt to look up the given name.

    The name is split into parts on the "." character and the root part
    is searched for in the "ns" dictionary, in globals() and finally in
    builtins.  Once the root part is found, attributes corresponding to the
    remainder of the name are looked up.  An exception is raised
    (explicity) if the root part cannot be found or (implicitly)
    if one of the remaining parts cannot be found.
    """

    parts = name.split('.')
    root = parts.pop(0)

    if root in ns:
        result = ns[root]
    elif root in globals():
        result = globals()[root]
    elif hasattr(builtins, root):
        result = getattr(builtins, root)
    else:
        raise Exception('cannot find "{0}"'.format(root))

    for part in parts:
        result = getattr(result, part)

    return result

def call_class_method(message):
    """Call the class method specified in the message.

    The context, if present in the message, is ignored.
    """

    cls =  _find_attr(message['class'])
    func = getattr(cls, message['name'])
    return _make_result(func(
        *(message['args'] if message['args'] is not None else ()),
        **(message['kwargs'] if message['kwargs'] is not None else {})))

def call_function(message):
    """Call the function specified in the message.

    The context, if present in the message, is ignored.
    """

    func = _find_attr(message['name'])
    return _make_result(func(
        *(message['args'] if message['args'] is not None else ()),
        **(message['kwargs'] if message['kwargs'] is not None else {})))

def call_method(message):
    """Call an object method.

    Works similarly to call_function.
    """

    obj = objects[message['number']]
    return _make_result(getattr(obj, message['name'])(
        *(message['args'] if message['args'] is not None else ()),
        **(message['kwargs'] if message['kwargs'] is not None else {})))

def construct_object(message):
    """Call an object constructor.

    Works similarly to call_function.
    """

    cls =  _find_attr(message['class'])
    return _make_result(cls(
        *(message['args'] if message['args'] is not None else ()),
        **(message['kwargs'] if message['kwargs'] is not None else {})))

def destroy_object(message):
    """Remove an object from the objects dictionary."""

    del objects[message['number']]
    return null_result

def get_attribute(message):
    """Get an attribute value from an object."""

    return _make_result(getattr(objects[message['number']], message['name']))

def get_value(message):
    """Get the value of a variable.

    If the variable name contains "."-separated components, then it is
    looked up using the _find_attr function.
    """

    (root, _, name) = message['name'].rpartition('.')

    if root:
        base = _find_attr(root)
    else:
        base = ns

    try:
        return _make_result(base[name])
    except TypeError:
        return _make_result(getattr(base, name))

def import_module(message):
    """Import a module or names from a module.

    Without arguments, the module is imported and the top level package
    name is inserted into the "ns" dictionary.

    With "args" specified, it is used as a list of names to import
    from the module, and those names are inserted into the "ns"
    dictionary.

    Currently any "kwargs" in the message are ignored.
    """

    if message['args']:
        # With arguments, emulate: from name import args

        mod = __import__(message['name'], fromlist=message['args'], level=0)
        for name in message['args']:
            ns[name] = getattr(mod, name)
    else:
        # Without arguments do plain import
        mod = __import__(message['name'], level=0)
        ns[mod.__name__] = mod

    return null_result

def set_attribute(message):
    """Set an attribute value of an object."""

    setattr(objects[message['number']], message['name'], message['value'])
    return null_result

def set_value(message):
    """Set the value of a variable.

    If the variable name contains "."-separated components, then it is
    looked up using the _find_attr function.
    """

    (root, _, name) = message['name'].rpartition('.')

    if root:
        base = _find_attr(root)
    else:
        base = ns

    try:
        base[name] = message['value']
    except TypeError:
        setattr(base, name, message['value'])

    return null_result
