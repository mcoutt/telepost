from django.db import models
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db import transaction

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fname = models.CharField(max_length=50, null=True, blank=True, default=None)
    lname = models.CharField(max_length=50, null=True, blank=True, default=None)
    email = models.CharField(max_length=50, unique=True, null=True, blank=True, default=None)
    token = models.CharField(max_length=50, unique=True, null=True, blank=True, default=None)
    telegram_id = models.CharField(max_length=50, unique=True, null=True, blank=True, default=None)
    telegram_chat_id = models.CharField(max_length=50, unique=True, null=True, blank=True, default=None)
    post_count = models.IntegerField(default=0, blank=True, null=True)

    max_post = models.IntegerField(default=0, blank=True, null=True)
    max_like = models.IntegerField(default=0, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['fname', 'lname']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
