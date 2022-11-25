from django.db import models
from django.apps import apps
from django.db.models.signals import post_save


class Category(models.Model):
    category = models.CharField(max_length=50, default="Test")

    def __str__(self):
        return self.category


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def on_delete(self) -> None:
        items = Item.objects.order_by('-item_id')[:self.item_id]

        for item in items:
            item.item_id -= 1

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


class Client(models.Model):
    place = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.place


class Transaction(models.Model):
    """ The transactions that we want to track primarily """

    trans_id = models.AutoField(primary_key=True, blank=True)
    quantity = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
    state = models.SmallIntegerField(default=0)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=False, null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)
    the_vendor = models.ForeignKey("accounts.Vendor", on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self) -> str:
        return "%s , %s , %s" % (self.item.name, self.client.place, self.time)
