from django.shortcuts import render
from django.contrib import messages

from groups.models import Group,GroupMember
from django.views import generic

from django.urls import reverse
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin


# Create your views here.
class CreateGroup(LoginRequiredMixin,generic.CreateView):
    model = Group
    fields = ('name','description')

class SingleGroup(generic.DetailView):
    model = Group
    context_object_name = 'group_detail'

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):

        return reverse('groups:single', kwargs = {'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        #get object of the group
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            #create a group and member, as we have to insert group id and user id
            GroupMember.objects.create(user=self.request.user,group=group)
        except:
            messages.warning(self.request,'User is already a member')
        else:
            messages.success(self.request,'User is now a member')

        return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )

        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
"""
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self,request,*args,**kwargs):

        try:
            #we always check via slug instead of id
            membership = GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get("slug")).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request,'User is not member of this group')
        else:
            membership.delete()
            message.success(self.request,'membership deleted')

        return super().get(request,*args,**kwargs)"""
