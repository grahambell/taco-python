# Taco Python transport module.
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

from codecs import utf_8_decode, utf_8_encode
from json import JSONDecoder, JSONEncoder


class TacoTransport():
    """Taco transport class.

    Implements the communication between Taco clients and servers.
    """

    def __init__(self, in_, out, from_obj=None, to_obj=None):
        """Constructs new TacoTransport object.

        Stores the input and output streams.  The "from_obj" and "to_obj"
        functions are used for the JSON encoder's "default" function
        and the JSON decoder's "object_hook" parameters respectively.
        """

        self.in_ = in_
        self.out = out

        self.encoder = JSONEncoder(default=from_obj)
        self.decoder = JSONDecoder(object_hook=to_obj)

    def read(self):
        """Read a message from the input stream.

        The decoded message is returned as a data structure, or
        None is returned if nothing was read.
        """

        text = ''
        while True:
            line = self.in_.readline()
            line = utf_8_decode(line)[0]

            if line == '' or line.startswith('// END'):
                break

            text += line

        if text == '':
            return None

        return self.decoder.decode(text)

    def write(self, message):
        """Write a message to the output stream."""

        message = self.encoder.encode(message)
        self.out.write(utf_8_encode(message)[0])
        self.out.write(utf_8_encode('\n// END\n')[0])
        self.out.flush()
