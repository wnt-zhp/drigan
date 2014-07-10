# -*- coding: utf-8 -*-

from django.forms import Field, ChoiceField
from django.utils.translation import ugettext_lazy
from dynamic_forms.fieldtype import create_dynamic_field_from_django_form


class StopienInstruktorski(ChoiceField):

    stopien_choices = (
        ("pwd", ugettext_lazy("Przewodniczka/Przewodnik")),
        ("phm", ugettext_lazy("Podharcmistrzyni/Podharcmistrz")),
        ("hm", ugettext_lazy("Harcmistrzyni/Harcmistrz")),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(self.stopien_choices, *args, **kwargs)


class StopienHarcerskiField(ChoiceField):

    stopien_choices = (
        ("mlo", ugettext_lazy("Ochotniczka/Młodzik")),
        ("wyw", ugettext_lazy("Tropicielka/Wywiadowca")),
        ("odkr", ugettext_lazy("Pionierka/Odkrywca")),
        ("sam", ugettext_lazy("Samarytanka/Ćwik")),
        ("ho", ugettext_lazy("Harcerka Orla/Harcerz Orli")),
        ("hr", ugettext_lazy("Harcerka Rzeczypospolitej/Harcerz Rzeczypospolitej")),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(self.stopien_choices, *args, **kwargs)

create_dynamic_field_from_django_form(StopienInstruktorski, ugettext_lazy('Stopień Harcerski'))
create_dynamic_field_from_django_form(StopienHarcerskiField, ugettext_lazy('Stopień Instruktorski'))
