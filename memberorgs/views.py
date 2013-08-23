# Create your views here.
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group

from userprofile.models import Profile
from memberorgs.models import MemOrg, MemOrgForm, NewAdminForm
from announce.models import Template

@permission_required('memberorgs.auth')
def index(request):
	if request.user.has_perm('memberorgs.uniauth'):
		memorgs_list = MemOrg.objects.all()
	else:
		memorg_id = request.user.profile_set.get().member_organization.id
		return HttpResponseRedirect(reverse('memorgs:detailmemorg', args=(memorg_id,)))
	return render(request, 'memberorgs/index.html', {'memorgs':memorgs_list})


@permission_required('memberorgs.uniauth')
def newMemOrg(request):
	if request.method == "POST":
		form = MemOrgForm(request.POST)
		if form.is_valid():
			new_save = form.save()
			new_save.save()
			new_template = Template(template_name="Default Template", member_organization=new_save,
				body="<html><body><h3 style='text-align:center;color:green'>{{glean.title}}</h3><p>{{glean.description}}</p><p>{{custom}}</p><p>For more information, click on the {{info}} link!</p><p>To no longer receive emails about gleaning, click on the {{unsubscribe}} link.</p></body></html>",
				default=True)
			new_template.save()
			return HttpResponseRedirect(reverse('memorgs:detailmemorg', args=(new_save.id,) ))
		else:
			return render(request, 'memberorgs/new_memorg.html', {'form':form, 'error':'Your Member Organization Form Was Not Valid'})
	else:
		form = MemOrgForm()
		return render(request, 'memberorgs/new_memorg.html', {'form':form})

@permission_required('memberorgs.auth')
def editMemOrg(request, memorg_id):
	memorg = get_object_or_404(MemOrg, pk=memorg_id)
	if memorg != request.user.profile_set.get().member_organization and not request.user.has_perm('memberorgs.uniauth'):
		return HttpResponseRedirect(reverse('memorgs:detailmemorg', args=(memorg.id,)))
	if request.method == "POST":
		form = MemOrgForm(request.POST)
		if form.is_valid():
			new_save = form.save(commit=False)
			new_save.id = memorg_id
			new_save.created = memorg.created
			new_save.save()
			return HttpResponseRedirect(reverse('memorgs:index'))
		else:
			return render(request, 'memberorgs/edit_memorg.html', {'form':form, 'memorg':memorg, 'error':'form needs some work', 'editmode':True})
	form = MemOrgForm(instance = memorg)

	return render(request, 'memberorgs/edit_memorg.html', {'form':form, 'memorg':memorg, 'editmode':True})

def detailMemOrg(request, memorg_id):
	memorg = get_object_or_404(MemOrg, pk=memorg_id)
	return render(request, 'memberorgs/detail_memorg.html', {'memorg':memorg})

@permission_required('memberorgs.uniauth')
def newMemOrgAndSuperUser(request):
	if request.method == "POST":
		form = MemOrgForm(request.POST)
		if form.is_valid():
			new_save = form.save()
			new_save.save()
			new_template = Template(template_name="Default Template", member_organization=new_save,
				body="<html><body><h3 style='text-align:center;color:green'>{{glean.title}}</h3><p>{{glean.description}}</p><p>{{custom}}</p><p>For more information, click on the {{info}} link!</p><p>To no longer receive emails about gleaning, click on the {{unsubscribe}} link.</p></body></html>",
				default=True)
			new_template.save()
			return HttpResponseRedirect(reverse('memorgs:detailmemorg', args=(new_save.id,) ))
		else:
			return render(request, 'memberorgs/new_memorg.html', {'form':form, 'error':'Your Member Organization Form Was Not Valid'})
	else:
		form = MemOrgForm()
		return render(request, 'memberorgs/new_memorg.html', {'form':form})

@permission_required('memberorgs.auth')
def newAdministrator(request, memorg_id):
	member_organization = get_object_or_404(MemOrg, pk=memorg_id)
	profile = request.user.profile_set.get()
	if not request.user.has_perm('memberorgs.uniauth') and member_organization != profile.member_organization:
		return HttpResponseRedirect(reverse('memorgs:detailmemorg', args=(memorg_id,)))
	if request.method == 'POST':
		form = NewAdminForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
			new_profile = Profile(user=new_user,
								first_name=form.cleaned_data['first_name'],
								last_name=form.cleaned_data['last_name'],
								phone=form.cleaned_data['phone'],
								member_organization=form.cleaned_data['member_organization']
								)
			new_profile.save()
			for county in member_organization.counties.all():
				new_profile.counties.add(county)
			member_organization.volunteers.add(new_user)
			
			if member_organization.name == 'Salvation Farms': #hard coded group. slap on the wrist.
				if form.cleaned_data['access_level'] == 'PD':
					sal = Group.objects.get(name="Salvation Farms Administrator")
					new_user.groups.add(sal)		
				else:
					salc = Group.objects.get(name="Salvation Farms Coordinator")
					new_user.groups.add(salc)
			else:
				if form.cleaned_data['access_level'] == 'PD':		
					ed = Group.objects.get(name="Member Organization Executive Director")
					new_user.groups.add(ed)
				else:
					memc = Group.objects.get(name="Member Organization Glean Coordinator")
					new_user.groups.add(memc)

			if request.POST['action'] == 'Save':
				return HttpResponseRedirect(reverse('memorgs:detailmemorg', args=(memorg_id,)))
			else:
				form = NewAdminForm()
				form.fields['member_organization'].queryset = MemOrg.objects.filter(pk=memorg_id)
				notice = 'Administrator account ' + new_user.username + ' has been created'
				return render(request, 'memberorgs/newadmin.html', {'form':form, 'notice':notice})				
		else:
			return HttpResponse('form.is_not_valid :(')

	form = NewAdminForm()
	form.fields['member_organization'].queryset = MemOrg.objects.filter(pk=memorg_id)
	return render(request, 'memberorgs/newadmin.html', {'form':form})


