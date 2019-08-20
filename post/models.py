from django.db import models
from user.models import User
import uuid


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True, default=None)
    description = models.CharField(max_length=50, null=True, blank=True, default=None)

    like = models.IntegerField(default=0, blank=True, null=True)
    unlike = models.IntegerField(default=0, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def get_user(self):
        user = User.objects.get(id=self.user_id)
        return user

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = "Post's"

    def __str__(self):
        return "post"
