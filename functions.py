

def primary_source(glean):
	if glean.counties.all():
		return glean
	elif glean.farm_location and glean.farm_location.counties.all():
		return glean.farm_location
	elif glean.farm and glean.farm.counties.all():
		return glean.farm
	else:
		return glean

def primary_address(glean):
	if glean.address_one:
		return glean
	elif glean.farm_location and glean.farm_location.address_one:
		return glean.farm_location
	elif glean.farm and glean.farm.address_one:
		return glean.farm
	else:
		return None