# cidgets is short for custom widgets.
# yeah, I know.

from django.forms.extras.widgets import Widget

class DatePicker(Widget):
	#attrs = self.attrs
	def render(self, name, value, attrs=None):
		string = u'''
	     <div class="input-append datetimechoser">
	       <label for="{{ field.id_for_label }}"> {{ field.label_tag }}</label> <input id="{{ field.auto_id }}" maxlength=200 name="{{ field.name }}" data-format="MM/dd/yyyy hh:mm:ss" type="text" value="{{ field.value }}"></input>
	       <span class="add-on">
	       <i data-time-icon="icon-time" data-date-icon="icon-calendar"></i>
	       </span>
	     </div>
	   	'''
		return string

'''# This be how you put custom widgets into ModelForm subclasses:
from django.forms import ModelForm, Textarea
from myapp.models import Author

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'title', 'birth_date')
        widgets = {
            'name': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
'''