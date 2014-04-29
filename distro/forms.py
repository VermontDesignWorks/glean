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


WorkEventFormSet = modelformset_factory(WorkEvent, extra=10)

EditWorkEventFormSet = modelformset_factory(WorkEvent, extra=0)


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


class WorkEventForm(ModelForm):
    class Meta:
        model = WorkEvent
