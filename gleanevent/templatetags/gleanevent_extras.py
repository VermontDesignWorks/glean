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


@register.filter('newrow')
def newrow(my_iteration):
    counter = 1
    rowlength = 3
    while counter <= my_iteration:
        if counter == my_iteration:
            return True
        counter = counter + rowlength
    return False


@register.filter('endrow')
def endrow(my_iteration):
    counter = 3
    rowlength = 3
    while counter <= my_iteration:
        if counter == my_iteration:
            return True
        counter = counter + rowlength
    return False


@register.filter('formname')
def formname(my_text):
    my_text = 'New ' + my_text.split('Form')[0]
    return my_text