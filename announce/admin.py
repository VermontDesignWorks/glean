from django.contrib import admin
from announce.models import Announcement, Template, RecipientList

admin.site.register(Announcement)
admin.site.register(Template)
admin.site.register(RecipientList)