from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager


class CustomAccountManager(BaseUserManager):
    def create_user(self, phone, name, email=None, password=None):
        user = self.model(phone=phone, name=name,
                          email=email, password=password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, email=None, password=None):
        user = self.create_user(
            phone=phone, name=name, email=email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, phone_):
        print(phone_)
        return self.get(phone=phone_)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['name', 'password']
    USERNAME_FIELD = 'phone'

    objects = CustomAccountManager()

    def get_short_name(self):
        return self.name

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name + " " + self.phone
