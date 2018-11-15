=====
Usage
=====

To use Django Geonames Place in a project, add it to your `INSTALLED_APPS`:

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
    ]

