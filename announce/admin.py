from django.contrib import admin
from announce.models import Announcement, Template

admin.site.register(Announcement)
admin.site.register(Template)