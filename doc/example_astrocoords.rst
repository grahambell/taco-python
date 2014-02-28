Object-Oriented Perl: Astro::Coords
===================================

This example demonstrates interaction with object-oriented
Perl libraries via Taco.
The libraries `Astro::Coords`_, `Astro::Telescope`_ and
`DateTime`_ are used to perform some calculations
related to the position of Mars over Jodrell Bank
during the Queen's speech on Christmas Day, 2010.

.. _DateTime: http://search.cpan.org/perldoc?DateTime

.. _`Astro::Coords`: http://search.cpan.org/perldoc?Astro::Coords

.. _`Astro::Telescope`: http://search.cpan.org/perldoc?Astro::Telescope

.. currentmodule:: taco

* Construct `DateTime`_ object

    First we set up a :class:`~client.Taco` object running the default
    Taco server script implementation for Perl.
    The server is then instructed to load the `DateTime`_ module
    and to construct an instance of that class.
    A set of Python keyword arguments is given to the constructor
    and will be turned into a flattened list of keywords and values
    as required by the `DateTime`_ constructor.
    Finally the `DateTime`_ object's ``strftime`` method is called
    to allow us to check that the date has been set correctly.

    .. testcode::

        from taco import Taco
        taco = Taco(lang='perl')

        taco.import_module('DateTime')
        qs = taco.construct_object('DateTime', year=2010, month=12, day=25,
                                   hour=15, minute=0, second=0)
        print(
            qs.call_method('strftime', '%Y-%m-%d %H:%M:%S')
        )

    .. testoutput::

        2010-12-25 15:00:00

    .. note::

        The actual `DateTime`_ object will be stored in an object
        cache on the server side.
        The :class:`~object.TacoObject`
        simply refers to it by an object number.
        When the :class:`~object.TacoObject`'s ``__del__``
        method is called, a ``destroy_object`` action
        will be sent, allowing the object to be cleared
        from the cache.

* Construct `Astro::Coords`_ object for Mars

    Next we import the `Astro::Coords`_ module and construct an object
    representing the coordinates of Mars.
    Since we may want to construct several similar objects,
    we use the :meth:`~client.Taco.constructor` convenience
    method to get a callable which we can use to call the
    class constructor.

    .. testcode::

        taco.import_module('Astro::Coords')
        coords = taco.constructor('Astro::Coords')
        mars = coords(planet='mars')
        print(
            mars.call_method('name')
        )

    .. testoutput::

        mars

* Construct `Astro::Telescope`_ object and apply it to Mars

    The `Astro::Telescope`_ class offers information about
    a number of telescopes.
    It has a class method which can be used to fetch a list
    of supported telescope identifiers.
    This Perl method needs to be called in list context
    so we specify ``context='list'`` in the method call.
    If you come across a function or method which requires
    a keyword argument called ``context``, this facility can
    be disabled by setting the ``disable_context``
    attribute of the :class:`~client.Taco` object,
    for example by specifying ``disable_context=True``
    in its constructor.

    .. testcode::

        taco.import_module('Astro::Telescope')
        telescopes = taco.call_class_method('Astro::Telescope',
                                            'telNames', context='list')
        print('JODRELL1' in telescopes)

    .. testoutput::

        True

    Now that we have confirmed that the Perl module knows about
    Jodrell Bank, we can set this as the location in our object
    representing Mars.
    The Python positional argument ``'JODRELL1'`` to the
    :meth:`~client.Taco.construct_object`
    method is passed to the Perl constructor at the start of its
    list of arguments.

    In this example, :meth:`~client.Taco.construct_object`
    will return a :class:`~object.TacoObject`,
    but when this is passed to another Taco method
    --- in this case :meth:`~object.TacoObject.call_method` ---
    it will automatically be converted to a reference to
    the object in the cache on the server side.

    We also need to set the date and time, which we can do by
    calling the `Astro::Coords`_ object's ``datetime`` method.
    However as we will want to be able to repeat this easily,
    we can use the convenience routine :meth:`~object.TacoObject.method`
    to get a Python callable for it.
    This can then be called with the object representing the
    date and time of the Queen's speech, which is again
    automatically converted to a reference to the corresponding
    Perl object.

    Finally we can have our `Astro::Coords`_ object calculate the
    elevation of Mars for this time and place.

    .. testcode::

        mars.call_method('telescope',
                         taco.construct_object('Astro::Telescope', 'JODRELL1'))
        datetime = mars.method('datetime')
        datetime(qs)
        print('{0:.1f}'.format(
            mars.call_method('el', format='degrees')
        ))

    .. testoutput::

        8.2

* Investigate the transit time

    So Mars was above the horizon (positive elevation), but it was still
    pretty low in the sky.
    We can have `Astro::Coords`_ determine the transit time --- the time
    at which it was highest.
    (In this method call, ``event=0`` requests the nearest transit,
    either before or after the currently configured time.)

    .. testcode::

        mt = mars.call_method('meridian_time', event=0)
        print(
            type(mt)
        )
        print(
            mt.call_method('strftime','%H:%M')
        )

    .. testoutput::

        <class 'taco.object.TacoObject'>
        12:52

    .. note::

        The Perl ``meridian_time`` method has returned an
        object, which is now being referred to by a
        :class:`~object.TacoObject` instance.
        Taco handles objects returned from functions and methods
        in the same way as objects explicitly constructed
        with :meth:`~client.Taco.construct_object`.

    We can now set the Mars object's time to the meridian time
    using our convenience callable, and find the corresponding elevation.

    .. testcode::

        datetime(mt)
        print('{0:.1f}'.format(
            mars.call_method('el', format='degrees')
        ))

    .. testoutput::

        13.0

* Check the distance to the Sun

    As a final example, we will calculate the distance (across the sky)
    between Mars and the Sun.
    First we construct an object representing the Sun's position.

    .. testcode::

        sun = coords(planet='sun')
        print(
            sun.call_method('name')
        )

    .. testoutput::

        sun

    Then, after setting the Sun object to the same time,
    we can request the distance between the two objects.
    `Astro::Coords`_ returns the distance as another object,
    but we can call its ``degrees`` method to obtain
    a value in degrees.

    .. testcode::

        sun.call_method('datetime', mt)
        print('{0:.1f}'.format(
            mars.call_method('distance', sun).call_method('degrees')
        ))

    .. testoutput::

        9.9
