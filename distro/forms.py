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
from django.forms.models import modelformset_factory, inlineformset_factory, formset_factory
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
        self.helper.form_id = "id-custom-registration-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "",
            Fieldset(
                Row("deliver",
                    "pickup",
                    "field_glean",
                    "farm_pickup",
                    "farmers_market",
                    "drop_off",
                    "member_organization",
                    "del_or_pick",
                    "recipient",
                    "field_or_farm",
                    "date",
                    "farm",
                    "crops",
                    "pounds",
                    "other",
                    "containers")
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
    member_organization = forms.ChoiceField(choices=MemOrg.objects.all(), label="Member Organization")
    date_d = forms.DateField(label="Date of Distribution", widget=extras.SelectDateWidget(years=range(1950, datetime.date.today().year+50)), required=False)
    del_or_pick = forms.ChoiceField(
        choices=d_or_p,
        label="Distribution Method"
    )
    recipient = forms.ChoiceField(choices=RecipientSite.objects.all(), label="Recipient Site")
    field_or_farm = forms.ChoiceField(
        choices=g_or_p,
        label="Collection Method"
    )
    date = forms.DateField(label="Harvest Date", widget=extras.SelectDateWidget(years=range(1950, datetime.date.today().year+50)), required=False)
    farm = forms.ChoiceField(choices=Farm.objects.all(),label="Farm")
    crops = forms.CharField(max_length=50, label="Crop/Item")
    pounds = forms.CharField(max_length=5, label="pounds")
    other = forms.CharField(max_length=50, label="Count")
    containers = forms.CharField(max_length=20, label="containers")

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
