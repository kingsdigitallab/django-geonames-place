#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-geonames-place
------------

Tests for `django-geonames-place` models module.
"""

import geocoder
import unittest
from django.conf import settings
from django.db.utils import IntegrityError
from django.test import TestCase
from geonames_place.models import Place


@unittest.skipUnless(
    bool(settings.GEONAMES_KEY), 'No GEONAMES_KEY environment variable set')
class TestGeonames_place(TestCase):

    def setUp(self):
        self.geonames_id = 2635167
        self.geonames_address = 'United Kingdom'
        self.address = 'London'

    def test_save(self):
        p = Place(geonames_id=self.geonames_id)
        p.save()
        self.assertEquals(self.geonames_address, p.address)

        with self.assertRaises(IntegrityError):
            p = Place()
            p.save()

            p.geonames_id = self.geonames_id
            p.update_from_geonames = False
            p.save()

    def test_update_from_geonames(self):
        p = Place()
        p.hydrate_from_geonames()
        self.assertIsNone(p.address)

        p.geonames_id = self.geonames_id
        p.hydrate_from_geonames()
        self.assertEquals(self.geonames_address, p.address)

    def test__hydrate(self):
        p = Place(geonames_id=self.geonames_id)
        p._hydrate(None)
        self.assertIsNone(p.address)

        g = geocoder.geonames(
            p.geonames_id, key=settings.GEONAMES_KEY, method='details')

        p._hydrate(g)
        self.assertEquals(self.geonames_address, p.address)

    def test_create_or_update_from_geonames(self):
        self.assertEquals(0, Place.create_or_update_from_geonames(None))
        self.assertEquals(0, Place.create_or_update_from_geonames('lo'))
        self.assertEquals(settings.GEONAMES_MAX_RESULTS,
                          Place.create_or_update_from_geonames(self.address))
