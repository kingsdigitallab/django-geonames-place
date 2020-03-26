"""
test_django-geonames-place
------------

Tests for `django-geonames-place` views module.
"""

import unittest

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from geonames_place.models import Place


@unittest.skipUnless(
    settings.GEONAMES_KEY, 'No GEONAMES_KEY environment variable set')
class TestGeonamesPlaceViews(TestCase):

    def setUp(self):
        self.geonames_id = 2635167
        self.geonames_address = 'United Kingdom'
        self.address = 'London'

    def test_autocomplete_view(self):
        self.assertEqual(Place.objects.count(), 0)
        url = reverse('place_autocomplete')
        c = Client()
        response = c.get(url, {'term': 'Lo'})
        self.assertEqual(response.json()['results'], [])
        p = Place(geonames_id=self.geonames_id)
        p.save()
        self.assertEqual(Place.objects.count(), 1)
        response = c.get(url, {'term': 'London'})
        self.assertNotEqual(len(response.json()['results']), 0)
        # There are many places with London in the name, and they
        # should now be stored in the Place model, having been fetched
        # from Geonames.
        self.assertTrue(Place.objects.count() > 1)
