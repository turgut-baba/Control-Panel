from django.db import models
from django.apps import apps


class Category(models.Model):
    category = models.CharField(max_length=50)

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
