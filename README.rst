=====================
Django Geonames Place
=====================

.. image:: https://travis-ci.org/kingsdigitallab/django-geonames-place.svg?branch=master
        :target: https://travis-ci.org/kingsdigitallab/django-geonames-place

.. image:: https://codecov.io/gh/kingsdigitallab/django-geonames-place/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/kingsdigitallab/django-geonames-place

Application to access Geonames Places directly from Django.
The application can create places by using a geonames id or by using a search
address.

This application depends on the very useful
`Python Geocoder <https://geocoder.readthedocs.io/index.html>`_ library.

Documentation
-------------

The full documentation is at https://django-geonames-place.readthedocs.io.

Quickstart
----------

Install Django Geonames Place::

    pip install django-geonames-place

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'geonames_place.apps.GeonamesPlaceConfig',
        ...
    )

Add the settings `GEONAMES_KEY` and `GEONAMES_MAX_RESULTS`. The `GEONAMES_KEY`
is your Geoname API key, and the `GEONAMES_MAX_RESULTS` is used to set the
maximum number of results when searching Geonames.

.. code-block:: python

    GEONAMES_KEY = '<GEONAMES_USERNAME>'
    GEONAMES_MAX_RESULTS = 10

To reference Geonames Place in your models:

.. code-block:: python

    from django.db import models
    from geonames_place.models import Place


    class MyModel(models.Model):
        ...
        place = models.ForeignKey(Place, on_delete=models.CASCADE)
        ...


Running Tests
-------------

Does the code actually work?

::

    export GEONAMES_KEY=<GEONAMES_USERNAME>
    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
