# Taco Python client module.
# Copyright (C) 2014 Graham Bell
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


class TacoError(Exception):
    """Base class for specific Taco client exceptions.

    Note that the client can also raise general exceptions,
    such as ValueError, if its methods are called with invalid
    arguments.
    """

    pass


class TacoReceivedError(TacoError):
    """An exception raised by the Taco client.

    Raised if the client receives an exception action.  The exception
    message will contain any message text received in the exception action.
    """

    pass


class TacoUnknownActionError(TacoError):
    """An exception raised by the Taco client.

    Raised if the client receives an action of an unknown type.
    """

    pass
