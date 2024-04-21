from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class VerificationCode(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    vc_code = models.CharField(max_length=6)
    time_generated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}, Code: {self.vc_code}"


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.first_name = 'admin'
        user.last_name = 'admin'
        user.role = 'superuser'
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    # required fields
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    password = models.CharField(max_length=20, blank=True)
    role = models.CharField(default='normal-user', max_length=20, verbose_name='role')
    locations = models.ManyToManyField('inventory.Location', blank=True, related_name='users')

    # optional fields
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='users/images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # auto-generate fields
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # For checking permissions. to keep it simple all admin have ALL permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Say whether this user has permission to view this app
    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
