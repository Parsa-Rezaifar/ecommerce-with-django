from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,PermissionsMixin
from . managers import UserManager

# Create your models here.

class User(AbstractBaseUser,PermissionsMixin) :

    email = models.EmailField(max_length=255,unique=True)
    phone_number = models.CharField(max_length=11,unique=True)
    full_name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number' # USERNAME_FIELD IS STR(ONR PART)
    REQUIRED_FIELDS = ['email', 'full_name'] #REQUIRED_FIELDS IS LIST

    objects = UserManager()

    def __str__(self) :
        return self.email

    @property
    def is_staff(self) :
        return self.is_admin

class OtpCode(models.Model) :

    phone_number = models.CharField(max_length=11,unique=True)
    code = models.PositiveSmallIntegerField()
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f'{self.code} sent to {self.phone_number}'