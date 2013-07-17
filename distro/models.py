from django.db import models

from memberorgs.models import MemOrg
from farms.models import Farm
from recipientsite.models import Site
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
	g_or_p = (
		(field_glean, 'Field Glean'),
		(farm_pickup, 'Farm Pickup')
	)
	member_organization = models.ForeignKey(MemOrg, verbose_name = "Member Organization", editable = False)
	date = models.DateField()
	farm = models.ForeignKey(Farm, null=True, blank=True)
	crops = models.CharField(max_length=50, blank=True, null=True)
	pounds = models.CharField(max_length=5, default=0)
	other = models.CharField(max_length=50, blank=True, null=True)
	containers = models.CharField(max_length=20, blank=True, null=True)
	recipient = models.ForeignKey(Site, verbose_name = "Recipient Site")
	del_or_pick = models.CharField(max_length=2, choices=d_or_p, default='d')
	field_or_farm = models.CharField(max_length=1, choices=g_or_p, default='g')