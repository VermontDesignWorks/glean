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

from distro.models import WorkEvent
from django.forms.models import modelformset_factory

from announce.models import Template, Announcement


class TemplateForm(ModelForm):
    class Meta:
        model = Template


class PartialTemplateForm(ModelForm):
    class Meta:
        model = Template
        exclude = ('template_name',)


class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
