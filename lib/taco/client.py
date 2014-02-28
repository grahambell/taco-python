# Taco Python client module.
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

import subprocess

from taco.error import TacoReceivedError, TacoUnknownActionError
from taco.object import TacoObject
from taco.transport import TacoTransport


class Taco():
    """Taco client class.

    Example::

        from taco import Taco

        taco = Taco(lang='python')

        taco.import_module('time', 'sleep')
        taco.call_function('sleep', 5)
    """

    def __init__(self, lang=None, script=None, disable_context=False):
        """Construct new Taco client by connecting to a server instance.

        The server script can either be specified explicitly with the
        "script" argument, or the language can be given with the "lang"
        argument.  In that case the server script will be assumed to
        be named taco-language and install in your binary search path
        ($PATH). If neither of these arguments is given, then a
        ValueError will be raised.

        The server script will be launched using subprocess.Popen
        and a TacoTransport object will be connected to it.
        """

        if script is not None:
            scr = script
        elif lang is not None:
            scr = 'taco-' + lang
        else:
            raise ValueError('language or script not specified')

        self.disable_context = disable_context

        p = subprocess.Popen([scr],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)

        self.xp = self._construct_transport(p.stdout, p.stdin)

    def _construct_transport(self, in_, out):
        """Prepare a TacoTransport object for use with this client.

        from_obj and to_obj functions are passed to the TacoTransport
        constructor to allow the JSON encoder/decoder to deal with Taco
        object references.
        """

        def from_obj(obj):
            if isinstance(obj, TacoObject):
                return {'_Taco_Object_': obj.number}
            else:
                raise ValueError('can not send non-Taco object')

        def to_obj(dict_):
            if '_Taco_Object_' in dict_:
                return TacoObject(self, dict_['_Taco_Object_'])
            else:
                return dict_

        return TacoTransport(in_, out, from_obj, to_obj)

    def _interact(self, message):
        """Private general interaction method used to implement other methods.

        Writes the given message to the server and reads the response.
        If this is a result, then its value is returned.  If it is an
        exception, then a TacoError exception is raised.
        """

        self.xp.write(message)

        response = self.xp.read()

        action = response['action']

        if action == 'result':
            return response['result']
        elif action == 'exception':
            raise TacoReceivedError('received exception: ' +
                                    response['message'])
        else:
            raise TacoUnknownActionError('received unknown action: ' + action)

    def call_class_method(self, class_, name, *args, **kwargs):
        """Invoke a class method call in the connected server.

        The context (void / scalar / list) can be specified as a
        keyword argument "context" unless the "disable_context" attribute
        has been set.
        """

        if 'context' in kwargs and not self.disable_context:
            context = kwargs.pop('context')
        else:
            context = None

        return self._interact({
            'action': 'call_class_method',
            'class': class_,
            'name': name,
            'args': args,
            'kwargs': kwargs,
            'context': context,
        })

    def call_function(self, name, *args, **kwargs):
        """Invoke a function call in the connected server.

        The context (void / scalar / list) can be specified as a
        keyword argument "context" unless the "disable_context" attribute
        has been set.
        """

        if 'context' in kwargs and not self.disable_context:
            context = kwargs.pop('context')
        else:
            context = None

        return self._interact({
            'action': 'call_function',
            'name': name,
            'args': args,
            'kwargs': kwargs,
            'context': context,
        })

    def _call_method(self, number, name, *args, **kwargs):
        """Private method for TacoObjects to send the call_method action."""

        if 'context' in kwargs and not self.disable_context:
            context = kwargs.pop('context')
        else:
            context = None

        return self._interact({
            'action': 'call_method',
            'number': number,
            'name': name,
            'args': args,
            'kwargs': kwargs,
            'context': context,
        })

    def construct_object(self, class_, *args, **kwargs):
        """Invoke an object constructor.

        If successful, this should return a :class:`~taco.object.TacoObject`
        instance which references the new object.  The given arguments and
        keyword arguments are passed to the object constructor.
        """

        return self._interact({
            'action': 'construct_object',
            'class': class_,
            'args': args,
            'kwargs': kwargs,
        })

    def _destroy_object(self, number):
        """Private method for TacoObjects to send the destroy_object action."""
        self._interact({
            'action': 'destroy_object',
            'number': number,
        })

    def _get_attribute(self, number, name):
        """Private method for TacoObjects to send the get_attribute action."""
        return self._interact({
            'action': 'get_attribute',
            'number': number,
            'name': name,
        })

    def get_value(self, name):
        """Request the value of the given variable."""

        return self._interact({
            'action': 'get_value',
            'name': name,
        })

    def import_module(self, name, *args, **kwargs):
        """Instruct the server to load the specified module.

        The interpretation of the arguments depends on the language of
        the Taco server implementation.
        """

        self._interact({
            'action': 'import_module',
            'name': name,
            'args': args,
            'kwargs': kwargs,
        })

    def _set_attribute(self, number, name, value):
        """Private method for TacoObjects to send the set_attribute action."""
        self._interact({
            'action': 'set_attribute',
            'number': number,
            'name': name,
            'value': value,
        })

    def set_value(self, name, value):
        """Set the value of the given variable."""

        self._interact({
            'action': 'set_value',
            'name': name,
            'value': value,
        })

    def function(self, name):
        """Convience method giving a function which calls call_function.

        This example is equivalent to that given for this class::

            sleep = taco.function('sleep')
            sleep(5)
        """

        def func(*args, **kwargs):
            return self.call_function(name, *args, **kwargs)

        return func

    def constructor(self, class_):
        """Convience method giving a function which calls construct_object.

        For example constructing multiple datetime objects::

            taco.import_module('datetime', 'datetime')
            afd = taco.construct_object('datetime', 2000, 4, 1)

        Could be done more easily::

            datetime = taco.constructor('datetime')
            afd = datetime(2000, 4, 1)
        """

        def func(*args, **kwargs):
            return self.construct_object(class_, *args, **kwargs)

        return func
