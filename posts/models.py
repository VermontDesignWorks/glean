from django.db import models
from django.forms import ModelForm

from django.contrib.auth.models import User
from memberorgs.models import MemOrg

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField()
	excerpt = models.CharField(max_length=200, editable=False)
	created_by = models.ForeignKey(User, editable=False)
	datetime = models.DateTimeField(auto_now_add=True, editable=False)
	member_organization = models.ForeignKey(MemOrg, editable=False)

	class Meta:
		permissions = (
			("auth", "Member Organization Level Permissions"),
			("uniauth", "Universal Permission Level"),
		)

	def __unicode__(self):
		return self.datetime.strf('%Y/%m/%d') + self.member_organization.name + ' - ' + self.title

class PostForm(ModelForm):
	class Meta:
		model = Post