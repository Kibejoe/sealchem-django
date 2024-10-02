from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email: #if email is not defined
            raise ValueError('Email must be created')
        if not username:
            raise ValueError('User must have a username')
        
        user = self.model( # the self.model returns the user class the baseusermanager manages rather than referencing the class name as in Account below
            email = self.normalize_email(email), #format the email
            first_name = first_name,
            last_name = last_name,
            username = username
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username= username,
            password= password,
            first_name= first_name,
            last_name = last_name
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50)

    #Requireds
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' #field to be used as the unique identifier
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None): #if the user has permision theyre an admin and admin has all permissions
        return self.is_admin
    
    def has_module_perms(self, add_label): #user has permissions related to other django apps
        return True



