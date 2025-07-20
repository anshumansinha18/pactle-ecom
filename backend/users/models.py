from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from store.models import Product



class CartItems(models.Model):
    # since we are using CustomUser Model(not Django's default User Model), 
    # we will use our custom AUTH_USER_MODEL(defined in settings/base.py)
    # on_delete=models.CASCADE: if a user is deleted from db, all its cart items would be deleted
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Product Model: store/models.py(Product)
    # On Delete: if a product is deleted from db, it will be removed from user's cart also
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        email = self.normalize_email(email)   # normalize email
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"  #tells which field to use when logging in a user
    REQUIRED_FIELDS = ["email"]   # used when creating a user