from rest_framework import serializers

from .models import ClassDescription, Country, FeatureClass, Place


class ClassDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassDescription
        fields = ['title']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'code']


class FeatureClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureClass
        fields = ['title']


class PlaceSerializer(serializers.ModelSerializer):
    class_description = ClassDescriptionSerializer(many=False, read_only=True)
    country = CountrySerializer(many=False, read_only=True)
    feature_class = FeatureClassSerializer(many=False, read_only=True)

    class Meta:
        model = Place
        fields = ['geonames_id', 'address', 'class_description',
                  'country', 'feature_class', 'lat', 'lon']
