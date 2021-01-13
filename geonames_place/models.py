# -*- coding: utf-8 -*-
import geocoder
from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class ClassDescription(TimeStampedModel):
    title = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Country(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=16, unique=True)

    class Meta:
        ordering = ["name", "code"]
        verbose_name_plural = "Countries"

    def __str__(self):
        return "{} ({})".format(self.name, self.code)


class FeatureClass(TimeStampedModel):
    title = models.CharField(max_length=16, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Place(TimeStampedModel):
    geonames_id = models.PositiveIntegerField(unique=True)
    update_from_geonames = models.BooleanField(default=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    class_description = models.ForeignKey(
        ClassDescription, blank=True, null=True, on_delete=models.CASCADE
    )
    country = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.CASCADE
    )
    feature_class = models.ForeignKey(
        FeatureClass, blank=True, null=True, on_delete=models.CASCADE
    )
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        ordering = ["address", "country"]

    def __str__(self):
        return "{}, {} in {}".format(self.address, self.class_description, self.country)

    def save(self, *args, **kwargs):
        if self.update_from_geonames:
            self.hydrate_from_geonames()
            self.update_from_geonames = False

        super().save(*args, **kwargs)

    @property
    def geo(self):
        return {"lat": self.lat, "lon": self.lon}

    def hydrate_from_geonames(self):
        if not self.geonames_id:
            return

        g = geocoder.geonames(
            self.geonames_id, key=settings.GEONAMES_KEY, method="details"
        )

        self._hydrate(g)

    def _hydrate(self, geoname):
        if not geoname:
            return

        self.address = geoname.address

        if geoname.class_description:
            cd, _ = ClassDescription.objects.get_or_create(
                title=geoname.class_description
            )
            self.class_description = cd

        if geoname.country and geoname.country_code:
            c, _ = Country.objects.get_or_create(
                name=geoname.country, code=geoname.country_code
            )
            self.country = c

        if geoname.feature_class:
            fc, _ = FeatureClass.objects.get_or_create(title=geoname.feature_class)
            self.feature_class = fc

        self.lat = geoname.lat

        if "lon" in geoname.fieldnames:
            self.lon = geoname.lon
        else:
            self.lon = geoname.lng

    @staticmethod
    def create_or_update_from_geonames(address, country_code=None):
        count = 0

        if not address:
            return count

        if len(address) < 3:
            return count

        options = {
            "key": settings.GEONAMES_KEY,
            "maxRows": settings.GEONAMES_MAX_RESULTS,
        }

        if country_code:
            options["country"] = country_code

        geonames = geocoder.geonames(address, **options)

        for g in geonames:
            p, _ = Place.objects.get_or_create(geonames_id=g.geonames_id)
            p._hydrate(g)
            p.save()

            count += 1

        return count

    @staticmethod
    def get_or_create_from_geonames(address, country_code=None):
        if not address:
            return None

        if len(address) < 3:
            return None

        options = {"key": settings.GEONAMES_KEY, "maxRows": 1}

        if country_code:
            options["country"] = country_code

        geonames = geocoder.geonames(address, **options)

        for g in geonames:
            p, _ = Place.objects.get_or_create(geonames_id=g.geonames_id)
            p._hydrate(g)
            p.save()

            return p

        return None
