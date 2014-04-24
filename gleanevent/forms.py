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
from gleanevent.models import GleanEvent, PostGlean
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
                        Div(InlineCheckboxes("vt_counties"),
                            InlineCheckboxes("ny_counties"),
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
                 "style='clear:both;' name='submit' value='Register'>")
        )

    time_of_day = forms.ChoiceField(label="&nbsp;",
                                    choices=TIME_OF_DAY,
                                    required=False)

    vt_counties = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="VT").order_by("name"),
        label="Counties in Vermont",
        required=False
    )
    ny_counties = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="NY").order_by("name"),
        label="Counties in New York",
        required=False
    )

    def get_county(self):
        if self.cleaned_data["vt_counties"].exists():
            return self.cleaned_data["vt_counties"][0]
        if self.cleaned_data["ny_counties"].exists():
            return self.cleaned_data["ny_counties"][0]

    class Meta:
        model = GleanEvent
        exclude = [
            'invited_volunteers',
            'attending_volunteers',
            'officiated_by'
        ]


class PostGleanForm(forms.ModelForm):
    class Meta:
        model = PostGlean

    def __init__(self, *args, **kwargs):
        super(PostGleanForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        helper.field_template = 'bootstrap3/layout/inline_field.html'
