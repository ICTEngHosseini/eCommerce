from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False,
                    is_admin=False):  # this function is take all things in the REQUIRED_FIELDS
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("User must have a password")
        # if not full_name:
        #     raise ValueError("User must have a correct Fullname")

        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password)  # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_admin=True,
            is_staff=True
        )
        return user


class User(AbstractBaseUser):
    # username = models.CharField(max_length=250)
    full_name = models.CharField(blank=True, null=True, max_length=150)
    email = models.EmailField(max_length=254, unique=True, default="example@email.com")
    active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff user none superuser
    admin = models.BooleanField(default=False)  # is superuser or not
    timestamp = models.DateTimeField(auto_now_add=True)
    # confirm = models.BooleanField(default=False)
    # confirm_date = models.DateTimeField(auto_now=False)

    USERNAME_FIELD = 'email'  # if you decision to login with username set the 'usename' on the 'email'
    # email(USERNAME_FIELD) and password are required by default
    REQUIRED_FIELDS = []  # that is a required fields --> ['full_name'] or samething else

    objects = UserManager()

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    # extend extra data


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.TimeField(auto_now=True)
    timestamp = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.email

