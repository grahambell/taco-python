# Taco Python object module.
# Copyright (C) 2013 Graham Bell
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


class TacoObject():
    """Taco object class.

    This class is used to represent objects by Taco actions.
    Instances of this class will returned by methods of Taco
    objects and should not normally be constructed explicitly.

    The objects reside on the server side and are referred to by instances
    of this class by their object number.  When these instances are
    destroyed the destroy_object action is sent automatically.
    """

    def __init__(self, client, number):
        """Construct new reference object.

        Stores a reference to the Taco client to allow actions to be
        sent via it.
        """

        self.client = client
        self.number = number

    def __del__(self):
        """Destroy the object by passing the destroy_object message to the
        server."""

        self.client._destroy_object(self.number)

    def call_method(self, *args, **kwargs):
        """Invoke the given method on the object.

        The first argument is the method name.

        The context (void / scalar / list) can be specified as a
        keyword argument "context" unless the "disable_context" attribute
        of the client has been set.
        """

        return self.client._call_method(self.number, *args, **kwargs)

    def get_attribute(self, *args, **kwargs):
        """Retrieve the value of the given attribute."""

        return self.client._get_attribute(self.number, *args, **kwargs)

    def set_attribute(self, *args, **kwargs):
        """Set the value of the given attribute."""

        return self.client._set_attribute(self.number, *args, **kwargs)

    def method(self, name):
        """Convenience method giving a function which calls a method.

        Returns a function which can be used to invoke a method on
        the server object. For example::

            strftime = afd.method('strftime')
            print(strftime('%Y-%m-%d'))
        """

        def func(*args, **kwargs):
            return self.call_method(name, *args, **kwargs)

        return func
