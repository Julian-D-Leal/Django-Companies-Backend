from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_admin=False, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_admin=is_admin, **extra_fields)
        if is_admin:
            user.set_password(password)  # Hash password for admins
            print(user.password)
        else:
            user.password = password   
        user.save(using=self._db)
        return user
    def verify_user(self, email, password):
        try:
            user = self.get(email=email)
            if user.check_password(password):
                return True
            else:
                return False
        except self.model.DoesNotExist:
            return False

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None 
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Company(models.Model):
    nit = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    

    def __str__(self):
        return self.name
    
class Product(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('COP', 'Colombian Peso'),
    ]
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='COP')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name