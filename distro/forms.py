from django.forms import ModelForm
from crispy_forms.bootstrap import (FieldWithButtons,
                                    InlineCheckboxes,
                                    StrictButton,
                                    AppendedText)
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
from django.forms.models import modelformset_factory
import time

from django.db import models

from django.contrib import admin

from memberorgs.models import MemOrg
from farms.models import Farm
from recipientsite.models import RecipientSite
from django.forms.widgets import TextInput


WorkEventFormSet = modelformset_factory(WorkEvent, extra=10)

EditWorkEventFormSet = modelformset_factory(WorkEvent, extra=0)


class DistroEntryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-custom-registration-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(


        )

    delivery = 'd'
    pickup = 'd'
    d_or_p = (
        (delivery, 'delivery'),
        (pickup, 'pickup')
    )
    field_glean = 'g'
    farm_pickup = 'p'
    farmers_market = 'f'
    drop_off = 'd'
    g_or_p = (
        (field_glean, 'Glean'),
        (farmers_market, "Farmer's Market"),
        (farm_pickup, 'Pickup'),
        (drop_off, "Drop off")
    )
    member_organization = models.ForeignKey(
        MemOrg, verbose_name="Member Organization", editable=False)
    date_d = models.DateField("Date of Distribution")
    del_or_pick = models.CharField(
        max_length=2,
        choices=d_or_p,
        default='d',
        verbose_name="Distribution Method"
    )
    recipient = models.ForeignKey(RecipientSite, verbose_name="Recipient Site")
    field_or_farm = models.CharField(
        max_length=1,
        choices=g_or_p,
        default='g',
        verbose_name="Collection Method"
    )
    date = models.DateField("Harvest Date")
    farm = models.ForeignKey(Farm, null=True, blank=True)
    crops = models.CharField(max_length=50, blank=True, null=True,
                             verbose_name="Crop/Item")
    pounds = models.CharField(max_length=5, blank=True, null=True)
    other = models.CharField(max_length=50, blank=True, null=True,
                             verbose_name="Count")
    containers = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        model = Distro


DistroEntryFormSet = inlineformset_factory(DistroEntryForm, Distro)


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
