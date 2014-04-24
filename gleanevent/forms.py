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
from Counties.models import County

from gleanevent.models import GleanEvent

from django import forms


class GleanForm(ModelForm):

    class Meta:
        model = GleanEvent
        exclude = [
            'invited_volunteers',
            'attending_volunteers',
            'officiated_by'
        ]


class PostGleanForm(ModelForm):
    class Meta:
        model = PostGlean

    def __init__(self, *args, **kwargs):
        super(PostGleanForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        helper.field_template = 'bootstrap3/layout/inline_field.html'
