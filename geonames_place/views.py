from functools import reduce
import operator

from django.contrib.admin.utils import lookup_needs_distinct
from django.core.exceptions import FieldDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from .admin import PlaceAdmin
from .models import Place


class PlaceAutocompleteJsonView(BaseListView):
    """View to provide autocompletion search results for Function objects.

    Adapted from django.contrib.admin.views.autocomplete and
    django.contrib.admin.options.

    """

    paginate_by = 20

    def get(self, request, *args, **kwargs):
        """Return a JsonResponse with search results of the form:

        {
            results: [{id: "123", text: "foo"}],
            pagination: {more: true}
        }

        """
        self.term = request.GET.get('term', '')
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {'id': str(obj.pk), 'text': str(obj)}
                for obj in context['object_list']
            ],
            'pagination': {'more': context['page_obj'].has_next()},
        })

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True):
        return Paginator(queryset, per_page, orphans, allow_empty_first_page)

    def get_queryset(self):
        queryset = Place.objects.get_queryset()
        queryset, use_distinct = self._get_search_results(queryset, self.term)
        if len(queryset) < 3 and len(self.term) > 3:
            Place.create_or_update_from_geonames(self.term)
            queryset, use_distinct = self._get_search_results(queryset,
                                                              self.term)
        return queryset

    def _get_search_results(self, queryset, search_term):
        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            # Use field_name if it includes a lookup.
            opts = queryset.model._meta
            lookup_fields = field_name.split(LOOKUP_SEP)
            # Go through the fields, following all relations.
            prev_field = None
            for path_part in lookup_fields:
                if path_part == 'pk':
                    path_part = opts.pk.name
                try:
                    field = opts.get_field(path_part)
                except FieldDoesNotExist:
                    # Use valid query lookups.
                    if prev_field and prev_field.get_lookup(path_part):
                        return field_name
                else:
                    prev_field = field
                    if hasattr(field, 'get_path_info'):
                        # Update opts to follow the relation.
                        opts = field.get_path_info()[-1].to_opts
            # Otherwise, use the field with icontains.
            return "%s__icontains" % field_name

        use_distinct = False
        search_fields = PlaceAdmin.search_fields
        if search_fields and search_term:
            orm_lookups = [construct_search(str(search_field))
                           for search_field in search_fields]
            for bit in search_term.split():
                or_queries = [Q(**{orm_lookup: bit})
                              for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
            use_distinct |= any(lookup_needs_distinct(Place._meta, search_spec)
                                for search_spec in orm_lookups)
        return queryset, use_distinct
