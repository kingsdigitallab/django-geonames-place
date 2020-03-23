import json

from django import forms
from django.urls import reverse


class AutocompleteMixin:

    """Select widget mixin that loads options from an autocomplete view
    via AJAX.

    Renders the necessary data attributes for select2.

    Adapted from django.contrib.admin.widgets.

    """

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs.setdefault('class', '')
        attrs.update({
            'class': (attrs['class'] + (' ' if attrs['class'] else '') +
                      'autocomplete'),
            'data-ajax--cache': 'true',
            'data-ajax--type': 'GET',
            'data-ajax--url': self.get_url(),
            'data-allow-clear': json.dumps(not self.is_required),
            'data-placeholder': 'Search GeoNames',
        })
        return attrs

    def optgroups(self, name, value, attr=None):
        """Return selected options based on the ModelChoiceIterator."""
        default = (None, [], 0)
        groups = [default]
        has_selected = False
        selected_choices = {
            str(v) for v in value
            if str(v) not in self.choices.field.empty_values
        }
        if not self.is_required and not self.allow_multiple_selected:
            default[1].append(self.create_option(name, '', '', False, 0))
        choices = (
            (obj.pk, self.choices.field.label_from_instance(obj))
            for obj in self.choices.queryset.filter(pk__in=selected_choices)
        )
        for option_value, option_label in choices:
            selected = (
                str(option_value) in value and
                (has_selected is False or self.allow_multiple_selected)
            )
            has_selected |= selected
            index = len(default[1])
            subgroup = default[1]
            subgroup.append(
                self.create_option(name, option_value, option_label,
                                   selected_choices, index))
        return groups


class PlaceSelect(AutocompleteMixin, forms.Select):

    def get_url(self):
        return reverse('geonames_place:place_autocomplete')
