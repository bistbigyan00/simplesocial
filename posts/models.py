from django.db import models
from groups.models import Group, GroupMember

from django.utils.text import slugify
from django.urls import reverse

from django.contrib.auth import get_user_model
import misaka

#getting user
User = get_user_model()

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,related_name = 'posts',on_delete=models.CASCADE)
    group = models.ForeignKey(Group,related_name = 'posts', on_delete=models.CASCADE, null = True, blank = True)
    message = models.TextField()
    message_html = models.TextField(editable = False)
    created_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.user

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('posts:single',kwargs = {'pk':self.pk,'username':self.user.username})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user','message']
