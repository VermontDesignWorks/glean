# Create your views here.
import time
import datetime


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

from django.contrib.auth.decorators import permission_required

from posts.models import Post, PostForm

@permission_required('posts.uniauth')
def index(request):
	if request.user.has_perm('posts.uniauth'):
		posts_list = Post.objects.all()
	else:
		posts_list = Post.objects.filter(member_organization=request.user.profile_set.get().member_organization.id)
		# post_id = request.user.profile_set.get().member_organization.id
		# return HttpResponseRedirect(reverse('posts:detailpost', args=(post_id,)))
	return render(request, 'posts/index.html', {'blog_posts':posts_list})

@permission_required('posts.uniauth')
def newPost(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			new_save = form.save(commit=False)
			new_save.member_organization = request.user.profile_set.get().member_organization
			if len(new_save.body) > 200:
				new_save.excerpt = new_save.body[:197] + '...'
			else:
				new_save.excerpt = new_save.body
			new_save.created_by = request.user
			new_save.save()
			return HttpResponseRedirect(reverse('posts:detailpost', args=(new_save.id,)))
		else:
			return render(request, 'posts/new_post.html', {'form':form, 'error':'Your Member Organization Form Was Not Valid'})
	else:
		form = PostForm()
		return render(request, 'posts/new_post.html', {'form':form})

@permission_required('posts.uniauth')
def editPost(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	if post != request.user.profile_set.get().member_organization and not request.user.has_perm('posts.uniauth'):
		return HttpResponseRedirect(reverse('posts:post', args=(post.id,)))
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			new_save = form.save(commit=False)
			new_save.id = post_id
			new_save.datetime = post.datetime
			new_save.member_organization = request.user.profile_set.get().member_organization
			if len(new_save.body) > 200:
				new_save.excerpt = new_save.body[:197] + '...'
			else:
				new_save.excerpt = new_save.body
			new_save.created_by = request.user
			new_save.save()
			return HttpResponseRedirect(reverse('posts:index'))
		else:
			return render(request, 'posts/edit_post.html', {'form':form, 'post':post, 'error':'form needs some work', 'editmode':True})
	form = PostForm(instance = post)

	return render(request, 'posts/edit_post.html', {'form':form, 'post':post, 'editmode':True})

def detailPost(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	return render(request, 'posts/detail_post.html', {'post':post})

#== Delete Post View ==#
@permission_required('posts.uniauth')
def deletePost(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	if post.member_organization != request.user.profile_set.get().member_organization and not request.user.has_perm('posts.uniauth'):
		return HttpResponseRedirect(reverse('posts:index'))
	if request.method == 'POST':
		post.delete()
		return HttpResponseRedirect(reverse('posts:index'))
	else:
		return render(request, 'posts/delete_post.html', {'post':post})