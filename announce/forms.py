from django.forms import ModelForm
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

from distro.models import WorkEvent
from django.forms.models import modelformset_factory

from announce.models import Template, Announcement
from memberorgs.models import MemOrg


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


class EditTemplateForm(ModelForm):
    'The class based form for editing a template'
    def __init__(self, *args, **kwargs):
        super(EditTemplateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-new-template-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row("template_name"),
                Row("body"),
                Row("default"),
                HTML("<input type='submit' "
                     "class='glean-button green-button' "
                     "name='submit' value='Save Changes'>")
            )
        )
    template_name = forms.CharField(label='Name: ', max_length=200)
    member_organization = forms.ModelChoiceField(
        label='Member Org',
        queryset=MemOrg.objects.all(),
        required=False)
    body = forms.CharField(
        label='Body: ',
        widget=forms.Textarea(
            attrs={'cols': '300', 'rows': '20', 'style': 'width: 650px'}),
        required=False)
    default = forms.BooleanField(label='Set as default template ', required=False)

    class Meta:
        model = Template
        exclude = ("member_organization",)


class NewTemplateForm(ModelForm):
    'The class based form for creating a new template'
    def __init__(self, *args, **kwargs):
        super(NewTemplateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-edit-template-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row("template_name"),
                Row("body"),
                Row("default"),
                HTML("<input type='submit' "
                     "class='glean-button green-button' "
                     "name='submit' value='Save Changes'>")
            )
        )
    template_name = forms.CharField(label='Name: ', max_length=200)
    member_organization = forms.ModelChoiceField(
        label='Member Org',
        queryset=MemOrg.objects.all(),
        required=False)
    body = forms.CharField(
        label='Body: ',
        widget=forms.Textarea(
            attrs={'cols': '300', 'rows': '20', 'style': 'width: 650px'}),
        required=False)
    default = forms.BooleanField(label='Set as default template ', required=False)

    class Meta:
        model = Template
        exclude = ("member_organization",)
