from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.apps import apps
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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


class Vendor(AbstractBaseUser):

    """ To showcase who did the transactions and monitor their movements"""

    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(max_length=250)
    desc = models.TextField(max_length=250)
    auth_level = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)])
    is_staff = models.BooleanField()
    is_active = models.BooleanField(default=True)
    transaction_history = models.ForeignKey("stocks.Transaction", on_delete=models.CASCADE, blank=False, null=True)
    trendyol_id = models.SmallIntegerField(default=1234, validators=[MinValueValidator(0), MaxValueValidator(9999)])

    REQUIRED_FIELDS = ['auth_level']
    USERNAME_FIELD = "name"

    objects = UserManager()

    class Meta:
        app_label = "accounts"
        db_table = "accounts_vendor"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_staff = self.auth_level >= 2

    # these two methods are require to login super user from admin panel:
    def has_perm(self, perm, obj=None) -> bool:
        return self.auth_level >= 2

    def has_module_perms(self, app_label) -> bool:
        return self.auth_level >= 2

    def __str__(self) -> str:
        return "%s , %s " % (self.name, self.desc)

