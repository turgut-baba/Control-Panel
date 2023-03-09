from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.apps import apps
from stocks.models import Item
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from enum import Enum, unique


@unique
class AuthLevel(Enum):
    Customer = 1
    Vendor = 2
    VendorAdmin = 3
    Admin = 4
    Owner = 5
    Programmer = 6


class UserManager(BaseUserManager):
    """ We do this as a fallback and to implement our own """
    use_in_migrations = True

    # python manage.py createsuperuser
    def create_superuser(self, name, auth_level, password):
        user = self.model(
            name=name,
            is_staff=(auth_level >= 2),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(max_length=250)
    desc = models.TextField(max_length=250)
    auth_level = models.SmallIntegerField(default=0, validators=[MinValueValidator(AuthLevel.Customer.value),
                                                                 MaxValueValidator(AuthLevel.Programmer.value)])
    is_staff = models.BooleanField()
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['auth_level']
    USERNAME_FIELD = "name"

    objects = UserManager()

    class Meta:
        app_label = "accounts"
        db_table = "account"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_staff = self.auth_level >= AuthLevel.Admin.value

    # these two methods are require to login super user from admin panel:
    def has_perm(self, perm, obj=None) -> bool:
        return self.auth_level >= AuthLevel.Admin.value

    def has_module_perms(self, app_label) -> bool:
        return self.auth_level >= AuthLevel.Admin.value

    def __str__(self) -> str:
        return "%s , %s " % (self.name, self.desc)


class Vendor(User):
    class Meta:
        app_label = "accounts"
        db_table = "account_vendor"

    """ To showcase who did the transactions and monitor their movements"""
    transaction_history = models.ForeignKey("stocks.Transaction", on_delete=models.CASCADE, blank=False, null=True)
    trendyol_id = models.SmallIntegerField(default=1234, validators=[MinValueValidator(0), MaxValueValidator(9999)])
    sold_products = models.ManyToManyField(to=Item)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Settings(models.Model):
    # user = models.OneToOneField()
    ...
