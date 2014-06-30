import datetime
from django.forms import ModelForm
from django import forms
from crispy_forms.bootstrap import (FieldWithButtons,
                                    InlineCheckboxes,
                                    StrictButton,
                                    AppendedText
                                    )
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout,
                                 Fieldset,
                                 ButtonHolder,
                                 Field,
                                 Row,
                                 Submit,
                                 Div,
                                 HTML)


from distro.models import WorkEvent, Distro
from django.forms.models import (modelformset_factory, inlineformset_factory,
                                 formset_factory)
import time

from django.db import models

from django.contrib import admin

from memberorgs.models import MemOrg
from farms.models import Farm
from recipientsite.models import RecipientSite
from django.forms.widgets import TextInput
from django.forms import extras


WorkEventFormSet = modelformset_factory(WorkEvent, extra=10)

EditWorkEventFormSet = modelformset_factory(WorkEvent, extra=0)


class DistroEntryForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DistroEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-harvest-entry-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "",
            Fieldset(
                "",
                Div(Row(Field("date_d"),
                        "del_or_pick",
                        "recipient",
                        "field_or_farm",
                        Field("date"),
                        "farm",
                        "crops",
                        "pounds",
                        "other",
                        "containers"
                        ),
                    )
            )
        )

    delivery = 'd'
    pickup = 'd'
    d_or_p = (
        (delivery, 'delivery'),
        (pickup, 'pickup')
    )
    drop_off = 'd'
    field_glean = 'g'
    farm_pickup = 'p'
    farmers_market = 'f'
    g_or_p = (
        (field_glean, 'Glean'),
        (farmers_market, "Farmer's Market"),
        (farm_pickup, 'Pickup'),
        (drop_off, "Drop off")
    )
    member_organization = forms.ModelChoiceField(
        queryset=MemOrg.objects.all(),
        label="", widget=forms.HiddenInput(), required=False)
    date_d = forms.DateField(required=False, label="")
    del_or_pick = forms.ChoiceField(
        choices=d_or_p,
        label="",
        required=False
    )
    recipient = forms.ModelChoiceField(
        queryset=RecipientSite.objects.all(),
        label="",
        required=False)
    field_or_farm = forms.ChoiceField(
        choices=g_or_p,
        label="",
        required=False
    )
    date = forms.DateField(required=False, label="")
    farm = forms.ModelChoiceField(
        queryset=Farm.objects.all(),
        label="",
        required=False)
    crops = forms.CharField(max_length=50, label="", required=False)
    pounds = forms.CharField(max_length=5, label="", required=False)
    other = forms.CharField(max_length=50, label="", required=False)
    containers = forms.CharField(
        max_length=20, label="", required=False)

    class Meta:
        model = Distro


class WorkEventFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(WorkEventFormHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Row(
                "first_name",
                "last_name",
                "date",
                "time",
                "group",
                "members",
                "task",
                "miles",
                "notes"
                )
        )
        self.add_input(
            Submit(
                "Save",
                "Save",
                css_class="glean-button red-button no-margin"
            )
        )
        self.template = 'bootstrap/table_inline_formset.html'
