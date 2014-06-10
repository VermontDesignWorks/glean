# Create your views here.
import csv
from django.http import Http404

from django import forms

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from constants import VERMONT_COUNTIES
from memberorgs.models import MemOrg
from gleaning.customreg import ExtendedRegistrationForm

from userprofile.models import (Profile,
                                UserForm,
                                LoginForm,
                                EmailForm,
                                UniPromoteForm,
                                PromoteForm)
from userprofile.forms import (ProfileUpdateForm,
                               ProfileForm,
                               EditProfileForm,
                               AdminProfileForm,
                               UserEditForm)


from django.contrib import messages

from generic.mixins import SimpleLoginCheckForGenerics


@login_required
def userDetailEntry(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            if not Profile.objects.filter(user=request.user).exists():
                new_save = form.save(commit=False)
                new_save.user = request.user
                new_save.save()
            else:
                form = ProfileForm(
                    request.POST,
                    Profile.objects.filter(user=request.user).get()
                )
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request,
                          'userprofile/userdetailentry.html',
                          {'form': form, 'error': "form wasn't valid"})
    else:
        form = ProfileForm
        return render(request,
                      'userprofile/userdetailentry.html',
                      {'form': form, 'error': ''})


class ProfileUpdateView(SimpleLoginCheckForGenerics, generic.UpdateView):
    template_name = "userprofile/edit.html"
    model = Profile
    success_url = reverse_lazy("userprofile:selfedit")

    def get_object(self):
        return self.request.user.profile

    def post(self, request, *args, **kwargs):
        if self.request.POST.get("submit") == "Save Changes":
            self.object = self.get_object()
            return super(ProfileUpdateView, self).post(
                request, *args, **kwargs)
        elif self.request.POST.get("submit") == "change password":
            p1 = self.request.POST.get("password1")
            p2 = self.request.POST.get("password2")
            if p1 == p2:
                u = User.objects.get(pk=self.request.user.pk)
                u.set_password(self.request.POST.get("password1"))
                u.save()
                messages.add_message(
                    self.request, messages.INFO, "Password Reset.")
                return HttpResponseRedirect("/users/edit/")
            else:
                messages.add_message(
                    self.request, messages.INFO, "Password Reset Failed.")
                return HttpResponseRedirect("/users/edit/")

    def get_form_class(self):
        if self.request.user.has_perm('userprofile.auth'):
            return AdminProfileForm
        else:
            return ProfileUpdateForm


class AdminProfileUpdateView(generic.FormView):
    form_class = AdminProfileForm


class UserLists(SimpleLoginCheckForGenerics, generic.ListView):
    template_name = "userprofile/userLists.html"

    def get_queryset(self):
        user = self.request.user
        groups = Group.objects.all()
        volunteers = User.objects.exclude(
            groups__in=groups
        ).order_by("profile__last_name")
        if user.has_perm('userprofile.uniauth'):
            return volunteers
        else:
            memorg = user.profile.member_organization
            counties = memorg.counties.all()
            return volunteers.filter(
                profile__counties__in=counties
            ).distinct().order_by("profile__last_name")


class UserProfileDelete(SimpleLoginCheckForGenerics, generic.DeleteView):
    model = User
    template_name = "userprofile/delete.html"
    success_url = reverse_lazy("userprofile:userlists")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfileDelete, self).dispatch(*args, **kwargs)


@permission_required('userprofile.auth')
def userProfile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    member_organization = request.user.profile.member_organization
    users = []
    for county in request.user.profile.member_organization.counties.all():
        for user in User.objects.all():
            if county in user.counties.all():
                users.append(user)

    if request.user.has_perm('userprofile.uniauth'):
        pass
    elif user not in users:
        return HttpResponseRedirect(reverse('home'))
    person = Profile.objects.get(user=user)
    return render(request, 'userprofile/detail.html', {'person': person})


class UserProfileDetailView(SimpleLoginCheckForGenerics, generic.DetailView):
    model = User

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfileDetailView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'userprofile:userprofile', args=(self.kwargs["pk"],))

    def get_object(self, *args, **kwargs):
        obj = super(
            UserProfileDetailView,
            self
        ).get_object(*args, **kwargs)
        return obj.profile

    def get_template_names(self):
        if self.object.admin:
            return "userprofile/admin_detail.html"
        return "userprofile/detail.html"


class UserEdit(SimpleLoginCheckForGenerics, generic.UpdateView):
    model = User
    success_url = reverse_lazy("userprofile:useredit")
    template_name = "userprofile/edit.html"

    def get_form_class(self):
        if self.object.admin:
            return AdminProfileForm
        return UserEditForm

    def get_success_url(self):
        editpk = self.kwargs["pk"]
        objectpk = int(editpk)
        return reverse_lazy("userprofile:useredit", kwargs={'pk': objectpk})

    def post(self, request, *args, **kwargs):
        if self.request.POST.get("submit") == "Save Changes":
            self.object = self.get_object()
            return super(UserEdit, self).post(request, *args, **kwargs)
        elif self.request.POST.get("submit") == "change password":
            editpk = self.kwargs["pk"]
            objectpk = int(editpk)
            p1 = self.request.POST.get("password1")
            p2 = self.request.POST.get("password2")
            if p1 == p2:
                u = User.objects.get(pk=objectpk)
                u.set_password(p1)
                u.save()
                messages.add_message(
                    self.request, messages.INFO, "Password Reset.")
                return HttpResponseRedirect(
                    reverse('userprofile:useredit', kwargs={'pk': objectpk})
                )
            else:
                messages.add_message(
                    self.request, messages.INFO, "Password Reset Failed.")
                return HttpResponseRedirect(
                    reverse('userprofile:useredit', kwargs={'pk': objectpk})
                )

    def get_object(self):
        editpk = self.kwargs["pk"]
        objectpk = int(editpk)
        u = User.objects.get(pk=objectpk)
        return u.profile

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        editpk = self.kwargs["pk"]
        objectpk = int(editpk)
        self_user = self.request.user
        memorg = self_user.profile.member_organization
        if self_user.has_perm("userprofile.uniauth"):
            return super(UserEdit, self).dispatch(*args, **kwargs)
        elif self_user.has_perm("userprofile.auth"):
            userlist = []
            for user in User.objects.all():
                for county in memorg.counties.all():
                    if county in user.profile.counties.all():
                        if user.has_perm('userprofile.uniauth') is False:
                            userlist.append(user)
            currentuser = User.objects.get(pk=editpk)
            if currentuser in userlist:
                return super(UserEdit, self).dispatch(*args, **kwargs)
            else:
                raise Http404
        else:
            raise Http404


def emailEdit(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            form = EmailForm()
            return render(
                request,
                'userprofile/emailedit.html',
                {'error': "That's not a valid address", 'form': form})
    else:
        form = EmailForm()
        return render(request, 'userprofile/emailedit.html', {'form': form})


@permission_required('userprofile.auth')
def download(request):
    memorg = request.user.profile.member_organization
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=user_profiles.csv'

    # Create the CSV writer using the HttpResponse as the "file."
    writer = csv.writer(response)
    writer.writerow([
        'Username',
        'Email',
        'First Name',
        'Last Name',
        'Address',
        'Address (line two)',
        'City',
        'State',
        'Counties',
        'Age Bracket',
        'Phone',
        'Phone Type',
        'Contact Method',
        "Join Date",
        'EC First',
        'EC Last',
        'EC Phone',
        'EC Relationship',
        'Accepts Email',
    ])

    if request.user.has_perm('userprofile.uniauth'):
        groups = Group.objects.all()
        profiles = Profile.objects.exclude(user__groups__in=groups)
    else:
        profiles = Profile.objects.filter(counties__in=memorg.counties.all())
    for profile in profiles:
            writer.writerow([
                profile.user.username,
                profile.user.email,
                profile.first_name,
                profile.last_name,
                profile.address_one,
                profile.address_two,
                profile.city,
                profile.state,
                profile.counties.all(),
                profile.age,
                profile.phone,
                profile.get_phone_type_display(),
                profile.get_preferred_method_display(),
                profile.user.date_joined.strftime("%m/%d/%Y"),
                profile.ecfirst_name,
                profile.eclast_name,
                profile.ecphone,
                profile.ecrelationship,
                profile.accepts_email,
                ])

    return response


@permission_required('userprofile.auth')
def newUser(request):
    notice = ''
    if request.method == 'POST':
        form = ExtendedRegistrationForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password1']
            )
            profile = Profile(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                address_one=form.cleaned_data['address_one'],
                address_two=form.cleaned_data['address_two'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                age=form.cleaned_data['age'],
                phone=form.cleaned_data['phone'],
                phone_type=form.cleaned_data['phone_type'],
                preferred_method=form.cleaned_data['preferred_method'],
                ecfirst_name=form.cleaned_data['ecfirst_name'],
                eclast_name=form.cleaned_data['eclast_name'],
                ecrelationship=form.cleaned_data['ecrelationship'],
                user=new_user,
                waiver=form.cleaned_data['waiver'],
                agreement=form.cleaned_data['agreement'],
                photo_release=form.cleaned_data['photo_release'],
                opt_in=form.cleaned_data['opt_in'],
            )
            profile.save()

            for county in form.cleaned_data['vt_counties']:
                profile.counties.add(county)
            for county in form.cleaned_data['ny_counties']:
                profile.counties.add(county)
            notice = ('New Volunteer ' + profile.first_name +
                      ' ' + profile.last_name + ' has been created.')
            form = ExtendedRegistrationForm()
    else:
        form = ExtendedRegistrationForm()
    users = []
    if request.user.has_perm('userprofile.uniauth'):
        users = User.objects.all().order_by('-date_joined')[:20]
    else:
        for county in request.user.profile.member_organization.counties.all():
            for user in User.objects.all():
                if county in user.profile.counties.all():
                    users.append(user)
    return render(
        request,
        'userprofile/newuser.html',
        {'form': form, 'users': users, 'notice': notice})


@permission_required('userprofile.auth')
def userPromote(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = user.profile
    rq_memorg = request.user.profile.member_organization
    ed = Group.objects.get(name="Member Organization Executive Director")
    memc = Group.objects.get(name="Member Organization Glean Coordinator")
    sal = Group.objects.get(name="Salvation Farms Administrator")
    salc = Group.objects.get(name="Salvation Farms Coordinator")
    # return HttpResponse(ed in user.groups.all())
    executive = ed in user.groups.all() or sal in user.groups.all()

    admin = executive or memc in user.groups.all() or salc in user.groups.all()
    data = {'member_organization': profile.member_organization,
            'executive': executive,
            'promote': admin}
    member_organization = forms.ModelChoiceField(
        queryset=MemOrg.objects.all(),
        label="Member Organization",
        empty_label=None)

    if request.user.has_perm('userprofile.uniauth'):
        if request.method == 'POST':
            form = UniPromoteForm(request.POST)
            if form.is_valid():
                user.groups.clear()
                profile.member_organization = form.cleaned_data[
                    'member_organization']
                profile.save()
                if form.cleaned_data['promote']:
                    if form.cleaned_data['member_organization'] == rq_memorg:
                        if form.cleaned_data['executive']:
                            user.groups.add(sal)
                        else:
                            user.groups.add(salc)
                    else:
                        if form.cleaned_data['executive']:
                            user.groups.add(ed)
                        else:
                            user.groups.add(memc)
                    return HttpResponseRedirect(
                        reverse(
                            'userprofile:userprofile', args=(user_id,)))
                else:
                    return HttpResponseRedirect(
                        reverse(
                            'userprofile:userprofile', args=(user_id,)))
            else:
                return render(
                    request,
                    'userprofile/user_promote.html',
                    {'form': form})
        else:
            form = UniPromoteForm(data)

    else:
        if request.method == 'POST':
            form = PromoteForm(request.POST)
            if form.is_valid():
                if executive is False:
                    user.groups.clear()
                    if form.cleaned_data['promote']:
                        user.groups.add(memc)
                else:
                    return HttpResponseRedirect(
                        reverse('userprofile:userprofile', args=(user.id,)))
            return HttpResponseRedirect(
                reverse('userprofile:userprofile', args=(user_id,)))
        else:
            form = PromoteForm({'promote': admin})
    return render(request, 'userprofile/user_promote.html', {'form': form})


def newAdmin(request, memorg_id):
    pass


@permission_required('userprofile.auth')
def reaccept(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = Profile.objects.filter(user=user).get()
    if not profile.accepts_email:
        profile.accepts_email = True
        profile.save()
    return HttpResponseRedirect(
        reverse('userprofile:userprofile', args=(user_id,)))
