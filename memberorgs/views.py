# Create your views here.
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib.auth.decorators import permission_required

from memberorgs.models import MemOrg, MemOrgForm

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