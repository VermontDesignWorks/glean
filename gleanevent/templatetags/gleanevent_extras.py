#Experiment to filter forms by variable type
from django import template

register = template.Library()

@register.filter('klass')
def klass(ob):
    return ob.__class__.__name__


@register.filter('dater')
def dater(my_string):
    my_test = (my_string.find("date") or my_string.find("Date"))
    return my_test