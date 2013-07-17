# Create your views here.
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from memberorgs.models import MemOrg, MemOrgForm


def index(request):
	memorgs_list = MemOrg.objects.all()
	return render(request, 'memberorgs/index.html', {'memorgs':memorgs_list})

#@login_required
def newMemOrg(request):
	if request.method == "POST":
		form = MemOrgForm(request.POST)
		if form.is_valid():
			new_save = MemOrg(**form.cleaned_data)
			new_save.save()
			return HttpResponseRedirect(reverse('memorgs:detailmemorg', args=(new_save.id,) ))
		else:
			return render(request, 'memberorgs/new_memorg.html', {'form':form, 'error':'Your Member Organization Form Was Not Valid'})
	else:
		form = MemOrgForm()
		return render(request, 'memberorgs/new_memorg.html', {'form':form})

#@login_required
def editMemOrg(request, memorg_id):
	memorg = get_object_or_404(MemOrg, pk=memorg_id)
	if request.method == "POST":
		form = MemOrgForm(request.POST)
		if form.is_valid():
			new_save = MemOrg(**form.cleaned_data)
			new_save.id = memorg_id
			new_save.save()
			return HttpResponseRedirect(reverse('memorgs:index'))
		else:
			return render(request, 'memberorgs/edit_memorg.html', {'form':form, 'memorg':memorg, 'error':'form needs some work', 'editmode':True})
	form = MemOrgForm(instance = memorg)

	return render(request, 'memberorgs/edit_memorg.html', {'form':form, 'memorg':memorg, 'editmode':True})

def detailMemOrg(request, memorg_id):
	memorg = get_object_or_404(MemOrg, pk=memorg_id)
	return render(request, 'memberorgs/detail_memorg.html', {'memorg':memorg})