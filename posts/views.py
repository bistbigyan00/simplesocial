from django.shortcuts import render
from django.contrib import messages

from posts import models
from groups.models import Group,GroupMember

from posts import forms
from django.views import generic

from django.contrib import messages

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from django.contrib.auth import get_user_model

User = get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ('user','group')

    #We will be dividing with logged_in user group and other_user group
    #is user logged in show user group or show other group
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        self.get_user_group = Group.objects.filter(members__in=[self.request.user])
        context['get_user_group'] = self.get_user_group

        self.get_other_group = Group.objects.exclude(members__in=[self.request.user]) #id
        context['get_other_group'] = self.get_other_group

        return context

class UserPosts(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ('user','group')
    template_name = 'user_post_list.html'

    #how many post does that user have
    def get_queryset(self):

        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact = self.kwargs.get('username'))

        except User.DoesNotExist:
            raise Http404

        else:
            #user.posts.all() shows all the user post_user
            #but we need only posts of logged in user so
            #above query in try
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact = self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    model = models.Post
    fields = ('message','group')

    def form_valid(self,form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)

class PostDelete(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)
