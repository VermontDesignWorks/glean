import time

from django.db import models

from memberorgs.models import MemOrg
from farms.models import Farm
from recipientsite.models import RecipientSite
from django.forms.widgets import TextInput
# Create your models here.

class Distro(models.Model):
	delivery = 'd'
	pickup = 'd'
	d_or_p = (
		(delivery, 'delivery'),
		(pickup, 'pickup')
	)
	field_glean = 'g'
	farm_pickup = 'p'
	farmers_market = 'f'
	g_or_p = (
		(field_glean, 'Field Glean'),
		(farm_pickup, 'Farm Pickup'),
		(farmers_market, "Farmer's Market")
	)
	member_organization = models.ForeignKey(MemOrg, verbose_name = "Member Organization", editable = False)
	date = models.DateField()
	farm = models.ForeignKey(Farm, null=True, blank=True)
	crops = models.CharField(max_length=50, blank=True, null=True)
	pounds = models.CharField(max_length=5, default=0)
	other = models.CharField(max_length=50, blank=True, null=True)
	containers = models.CharField(max_length=20, blank=True, null=True)
	recipient = models.ForeignKey(RecipientSite, verbose_name = "Recipient Site")
	del_or_pick = models.CharField(max_length=2, choices=d_or_p, default='d')
	field_or_farm = models.CharField(max_length=1, choices=g_or_p, default='g')
	#created_by = models.ForeignKey(User, shiiite)

	class Meta:
		permissions = (
			("auth", "Member Organization Level Permissions"),
			("uniauth", "Universal Permission Level"),
		)
	

	def __unicode__(self):
		return self.member_organization.name + ' ' + self.date.strftime('%Y %m %d - %I:%M:%S %p') #+ ' ' + self.created_by.profile_set.first_name + ' ' + self.created_by.profile_set.last_name