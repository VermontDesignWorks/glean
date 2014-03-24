from django.forms import ModelForm
from django.forms.fields import ChoiceField

from farms.models import Farm


class FarmForm(ModelForm):
    class Meta:
        model = Farm
        exclude = ['farmers']