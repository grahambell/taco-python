Procedural Perl
===============

This example illustrates a how Taco can be used to interact with
procedural Perl modules --- importing them,
calling functions, and interacting with variables.

.. currentmodule:: taco

* Calling functions to perform calculations

    We begin by importing the :class:`~client.Taco` class and
    constructing an instance of it which launches a Perl
    sub-process.
    Now we can calculate the sine of 30 degrees by calling
    Perl's ``sin`` subroutine (from the ``CORE::`` namespace).
    This should give the expected value of a half.

    .. testsetup::

        from math import radians

    .. testcode::

        from taco import Taco

        taco = Taco(lang='perl')

        print('{0:.2f}'.format(
            taco.call_function('CORE::sin', radians(30))
        ))

    .. testoutput::

        0.50

* Importing modules

    To make use of routines from other modules, they must be
    imported into the Perl interpreter running in the sub-process.
    The appropriate action to do this can be sent using the
    :meth:`~client.Taco.import_module` method.
    In the case of the Perl server, any arguments to this
    method are passed to the equivalent of a ``use`` statement.
    This allows us to bring the ``md5_hex`` subroutine into
    the current scope.

    .. testcode::

        taco.import_module('Digest::MD5', 'md5_hex')
        print(
            taco.call_function('md5_hex', 'Hello from Taco')
        )

    .. testoutput::

        9442d82de2303664e42b60e103c0ead4

* A more convenient way to call functions

    Another way to call a function through Taco is by creating
    a convenience callable for it.
    The :meth:`~client.Taco.function` method, given the name of
    a function to be called, returns an object which can
    be called to invoke that function.

    .. testcode::

        md = taco.function('md5_hex')
        print(
            md('Useful for calling the same function multiple times')
        )

    .. testoutput::

        47a533e6b83934f58c976de5f2b2dc5a

* Getting values

    We can retrieve the value of variables using
    :meth:`~client.Taco.get_value`.
    In this example, importing the "English" module gives a readable name
    for the variable containing the operating system name.

    .. testcode::

        taco.import_module('English')
        print(
            taco.get_value('$OSNAME')
        )

    .. testoutput::

        linux

* Setting values

    :meth:`~client.Taco.set_value` can be used to assign a variable
    on the server side.
    In the case of Perl, setting the output field separator
    variable ``$,`` will configure the spacing between
    things which are printed out.

    .. testcode::

        taco.set_value('$,', '**')

    At this stage we can make use of some object-oriented
    code to check that the setting of ``$,`` has taken effect.
    For more information about using Taco with object-oriented
    Perl modules, see the
    :doc:`object-oriented Perl example <example_astrocoords>`.
    Here we print the strings ``'X'``, ``'Y'`` and ``'Z'``
    to an `IO::String`_ object and check the result.

    .. testcode::

        taco.import_module('IO::String')
        s = taco.construct_object('IO::String')
        s.call_method('print', 'X', 'Y', 'Z')
        s.call_method('pos', 0)
        print(s.call_method('getline'))

    .. testoutput::

        X**Y**Z

.. _`IO::String`: http://search.cpan.org/perldoc?IO::String
