Taco Module for Python
======================

Introduction
------------

.. starttacointro

Taco is a system for bridging between scripting languages.
Its goal is to allow you to call routines written for one language from
another.
It does this by running the second language interpreter in a sub-process,
and passing messages about actions to be performed inside that interpreter.

In principle, to interface scripting languages it might be preferable
to embed the interpreter for one as an extension of the other.
However this might not be convenient or possible,
and would need to be repeated for each combination of languages.
Instead Taco only requires a "client" module and "server" script
for each language, which should be straightforward to install,
and its messages are designed to be generic so that they
can be used between any combination of languages.

For more information about Taco, please see the
`Taco Homepage`_.

.. _`Taco Homepage`: http://grahambell.github.io/taco/

.. endtacointro

Examples
~~~~~~~~

Here are examples of the different types of responses
which may result from a Taco call:

.. starttacoreturn

* Function Results

    If you find that you need the weighted ``roll_dice()``
    function from the `Acme::Dice`_ Perl module,
    you can import it and call the function as follows:

    >>> from taco import Taco
    >>> taco = Taco(lang='perl')
    >>> taco.import_module('Acme::Dice', 'roll_dice')
    >>> taco.call_function('roll_dice', dice=1, sides=6, favor=6, bias=100)
    6

    In this example, instantiating a ``Taco`` object starts a
    sub-process running a Perl script.
    This "server" script then handles the instructions to
    import a module and call one of its functions,
    returning the value 6.

* Object References

    To allow the use of object-oriented modules such as
    `Acme::PricelessMethods`_,
    references to objects are returned
    as instances of the ``TacoObject`` class.

    >>> taco.import_module('Acme::PricelessMethods')
    >>> pm = taco.construct_object('Acme::PricelessMethods')
    >>> type(pm)
    <class 'taco.object.TacoObject'>

    These objects can be used to invoke further actions:

    >>> pm.call_method('is_machine_on')
    1

* Exceptions

    ``roll_dice()`` raises an exception if we try to roll more than 100 dice.
    The exception is caught and re-raised on the "client" side:

    >>> taco.call_function('roll_dice', dice=1000)
    Traceback (most recent call last):
    ...
    taco.error.TacoReceivedError: ... Really? Roll 1000 dice? ...

.. _Acme::Dice: http://search.cpan.org/perldoc?Acme::Dice

.. _Acme::PricelessMethods: http://search.cpan.org/perldoc?Acme::PricelessMethods

.. endtacoreturn

.. starttacoinstall

Installation
------------

.. highlight:: bash

The module can be installed using the ``setup.py`` script::

    python setup.py install

Before doing that, you might like to run the unit tests::

    PYTHONPATH=lib python -m unittest -v

For Python 2, it might be necessary to include the command ``discover``
after the ``unittest`` module name.
If successful you should see a number of test cases being run.

Integration Tests
~~~~~~~~~~~~~~~~~

This package also includes further integration tests which test
the complete system.
These tests are stored in files named ``ti_*.py`` to avoid them
being found by ``unittest`` discovery with its default
parameters.
They all use the Python "client" module but a variety
of "server" scripts.

* Python

  The tests using a Python "server" script can be run directly from this
  package::

    PYTHONPATH=lib python -m unittest discover -v -s 'ti-python' -p 'ti_*.py'

* Other Languages

  The following tests all require a Taco "server" script for the
  corresponding language to be installed in your search path.

  * Perl ::

      PYTHONPATH=lib python -m unittest discover -v -s 'ti-perl' -p 'ti_*.py'

.. endtacoinstall

License
-------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Additional Links
----------------

* `Documentation at Read the Docs <http://taco-module-for-python.readthedocs.org/en/latest/>`_
* `Repository at GitHub <https://github.com/grahambell/taco-python>`_
* `Taco Homepage`_
