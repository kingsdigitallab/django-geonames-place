from django.contrib import admin
from geonames_place.models import (ClassDescription, Country, FeatureClass,
                                   Place)


@admin.register(ClassDescription)
class ClassDescriptionAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']


@admin.register(FeatureClass)
class FeatureClassAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['class_description', 'country', 'feature_class']
    list_display = ['address', 'class_description', 'country']
    list_filter = ['class_description', 'country']
    search_fields = ['address', 'country__name', 'country__code']
