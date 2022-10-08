from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from enum import Enum, unique, auto

"""
# This is where we declare added stores.
@unique
class StoreID(Enum):
    Trendyol = 1
    Hepsiburada = 2
    GittiGidiyor = 3
    END = auto()
    # Don't forget to migrate after adding a new store.


class Store(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=50, default="")
    store_id = models.SmallIntegerField(default=0,
                                        validators=[MinValueValidator(0), MaxValueValidator(StoreID.END.value)]
                                        )
    seller_id = models.CharField(max_length=15, default="1234")

    def __str__(self) -> models.CharField:
        return self.name

"""
from django.db.models.signals import post_save


class Store(models.Model):
    ...


class Category(models.Model):
    name = models.CharField(max_length=50, default="Test")

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50, default="Test")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    stock = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    # @staticmethod
    def post_save(self, sender, instance, created, **kwargs):
        if instance.previous_state != instance.state or created:

            all_listings = Listing.objects.filter(item=self)

            for listing in all_listings:
                listing.stock = self.stock
                listing.save()

            all_bundles = Bundle.objects.all()

            for bundle in all_bundles:
                if self in bundle.items:
                    all_items = bundle.items.all()
                    lowest_stock = all_items[0].stock
                    for item in all_items:
                        if item.stock < lowest_stock:
                            lowest_stock = item.stock
                    if self.stock == lowest_stock:
                        bundle.stock = self.stock
                        bundle.save()

    def __str__(self):
        return self.name


class Bundle(models.Model):
    name = models.CharField(max_length=50, default="Test")
    items = models.ManyToManyField(Item)
    stock = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        all_items = self.items.all()

        lowest_stock = all_items[0]

        for item in all_items:
            if item.stock < lowest_stock.stock:
                lowest_stock.stock = item.stock

        self.stock = lowest_stock.stock
        self.save()

    def __str__(self):
        return self.name


class Listing(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=1)
    stock = models.IntegerField(default=0)
