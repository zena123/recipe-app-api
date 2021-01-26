from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ creates and saves new user """
        if not email:
            raise ValueError('users must have valid email address')
        # normalize_email: helper function comes with BaseUserManager
        user= self.model(email=self.normalize_email(email), **extra_fields)
        # need that helper function because our password is encrypted
        user.set_password(password)
        user.save(using=self.db) # for supporting multiple databases

        return user

    # no need to worry about extra_fields because we will create it with terminal
    def create_superuser(self, email, password):
        """ creates ans saves new superuser """
        user= self.create_user(email, password)
        user.is_staff = True
        user.is_superuser= True
        user.save(using=self._db)   # user must be saved because it was modified

        return user




class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports using email instead of username"""
    email= models.EmailField(max_length=255, unique=True)
    name= models.CharField(max_length=255)
    is_active= models.BooleanField(default=True)   # userin system is active or not. 
    is_staff= models.BooleanField(default=False)   # staff user need special command to be created

    objects=UserManager()

    # username by default is : username but we customised it
    USERNAME_FIELD='email'

