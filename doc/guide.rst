Guide
=====

.. currentmodule:: taco

Starting a Taco Session
-----------------------

A Taco "client" session is started by constructing a :class:`~client.Taco`
instance.
The constructor will run a Taco "server" script in a sub-process
and attach a :class:`~transport.TacoTransport` object to the
sub-process's standard input and standard output.

There are two ways to specify which "server" script to run:

* The ``lang`` option

    This just specifies the language which the script should be using.
    The script will be assumed to be called ``taco-lang``, where
    ``lang`` is the given language.  For example a :class:`~client.Taco`
    "client" constructed with ``Taco(lang='perl')`` will try to run
    a script called ``taco-perl``.
    This script must be present in your search path for this to
    be successful.

* The ``script`` option

    This option allows you to specify the name of the "server" script
    directly.
    For example some of the integration tests run the Python "server"
    script directly from this package using
    ``Taco(script='scripts/taco-python')``.

Actions
-------

The rôle of the :class:`~client.Taco` "client" class is to send actions
to the "server" script.
While the actions are intended to be generic,
the exact behavior will depend will depend on the "server"
script and what is suitable for its language.
The :class:`~server.TacoServer` documentation includes
some information about how the actions are implemented in
Python.

* Procedural Actions

    These are invoked by calling :class:`~client.Taco` methods directly.

    * :meth:`~client.Taco.call_class_method`
    * :meth:`~client.Taco.call_function`
    * :meth:`~client.Taco.construct_object`
    * :meth:`~client.Taco.get_value`
    * :meth:`~client.Taco.import_module`
    * :meth:`~client.Taco.set_value`


* Object-oriented Actions

    These are invoked via methods of :class:`~object.TacoObject` instances.

    * :meth:`~object.TacoObject.call_method`
    * :meth:`~object.TacoObject.get_attribute`
    * :meth:`~object.TacoObject.set_attribute`

* Convenience Methods

    These methods each return a callable which can be used to
    perform a Taco action in a more natural manner.

    * :meth:`~client.Taco.function`
    * :meth:`~client.Taco.constructor`
    * :meth:`~object.TacoObject.method`

Taco action messages typically include a list called ``args``
and a dictionary called ``kwargs``.
The Python :class:`~client.Taco` "client" fills these parameters from
the positional and keyword arguments of its method calls.

Return Values
-------------

The Taco system allows for the return of various responses to actions.
Here are some examples of Taco actions and the responses to them:

.. include:: ../README.rst
    :start-after: .. starttacoreturn
    :end-before: .. endtacoreturn
