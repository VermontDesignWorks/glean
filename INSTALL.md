# Installation

mkvirtualenv glean
pip install -r requirements.txt
python manage.py syncdb --migrate
python manage.py runserver

# Add a user as an admin

python manage.py shell_plus

MemOrg.objects.get(name__icontains='Salvation')
sal_farms = _
ben = User.objects.create(username='ben_glass')
Profile.objects.create(user=ben, member_organization=sal_farms)
sal_farms_permissions_group = Group.objects.filter(name='Salvation Farms Administrator')
ben.groups.add(sal_farms_permissions_group[0])
ben.set_password('mypass')
ben.save()
