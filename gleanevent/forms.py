from django import forms
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

from counties.models import County
from gleanevent.models import GleanEvent
from constants import STATES, TIME_OF_DAY


class GleanForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GleanForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-custom-registration-form"
        self.helper.form_method = "post"
        self.helper.form_show_errors = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Row("title", "date"),
                    Row("time", "time_of_day", "duration"),
                    Row("volunteers_needed"),
                    Row("farm", "farm_location"),
                    Row("address_one", "address_two"),
                    Row("city", "state", "zipcode"),
                    Fieldset(
                        "",
                        HTML("<label for='id_counties' class='" +
                             "control-label' style='width:466px;" +
                             "'>Counties</label>"),
                        Div(InlineCheckboxes("vt_counties_single"),
                            InlineCheckboxes("ny_counties_single"),
                            css_class="glean-form-checkboxes")
                    ),
                    css_class="glean-form-left pull-left"
                ),
                Div(
                    "description",
                    "directions",
                    "instructions",
                    css_class="glean-form-right pull-left"
                ),
                css_class="glean-form-container"
            ),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "style='clear:both;' name='submit' value=\"Ok, It's Ready\">")
        )

    time_of_day = forms.ChoiceField(label="&nbsp;",
                                    choices=TIME_OF_DAY,
                                    required=False)

    vt_counties_single = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="VT").order_by("name"),
        label="Counties in Vermont",
        required=False
    )
    ny_counties_single = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="NY").order_by("name"),
        label="Counties in New York",
        required=False
    )

    def save(self, *args, **kwargs):
        saved = super(GleanForm, self).save(*args, **kwargs)
        if 'vt_counties_single' in self.data:
            for pk in self.data.getlist('vt_counties_single'):
                county = County.objects.get(pk=pk)
                saved.counties = county
        if 'ny_counties_single' in self.data:
            for pk in self.data.getlist('ny_counties_single'):
                county = County.objects.get(pk=pk)
                saved.counties = county
        saved.save()
        return saved

    class Meta:
        model = GleanEvent
        exclude = [
            'invited_volunteers',
            'attending_volunteers',
            'officiated_by'
        ]
