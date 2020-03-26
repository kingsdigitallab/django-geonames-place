from django.urls import path

from . import views


app_name = 'geonames_place'
urlpatterns = [
    path('place_autocomplete/', views.PlaceAutocompleteJsonView.as_view(),
         name='place_autocomplete'),
]
