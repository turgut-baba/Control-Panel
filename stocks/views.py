from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Control_Panel import settings
from .models import Transaction, Item, Category
from .forms import ItemForm
from django.contrib import messages
import json
import os
from django.shortcuts import redirect


@user_passes_test(lambda u: u.auth_level >= 2)
def index(request: str) -> HttpResponse:
    transactions_by_index = Transaction.objects.order_by('-time')[:5]
    total_income, total_cost, total_earned = 0, 0, 0

    for tran in transactions_by_index:
        total_income += tran.item.price * tran.item.quantity
        total_cost += tran.item.cost * tran.item.quantity
        total_earned += (tran.item.price * tran.item.quantity) - (tran.item.cost * tran.item.quantity)

    context = {
        'latest_transactions': transactions_by_index,
        'income': total_income,
        'cost': total_cost,
        'earned': total_earned
    }
    return render(request, "index.html", context)


@user_passes_test(lambda u: u.auth_level >= 2)
def shipments(request: str) -> HttpResponse:
    transactions_by_index = Transaction.objects.order_by('-time')
    context = {
        'latest_transactions': transactions_by_index,
    }
    return render(request, "stocks/shipments.html", context)


@user_passes_test(lambda u: u.auth_level >= 2)
def item_view(request: str) -> HttpResponse:
    item_list = Item.objects.order_by('-ID')
    context = {
        'item_list': item_list,
        'item_size': len(item_list)
    }
    return render(request, "stocks/items.html", context)


@user_passes_test(lambda u: u.auth_level >= 2)
def add_item(request: str) -> HttpResponse:
    categories = Category.objects.order_by('-category')
    last_id = Item.objects.order_by('-ID')[:1]

    try:
        used_id = last_id[0].ID + 1
    except IndexError:
        used_id = 0

    context = {
        'categories': categories,
        'last_id': used_id
    }

    if request.method == "POST":
        new_item = ItemForm(request.POST)
        if new_item.is_valid():

            Item.objects.create(
                name=new_item.cleaned_data['name'],
                quantity=new_item.cleaned_data['quantity'],
                price=new_item.cleaned_data['price'],
                cost=new_item.cleaned_data['cost']
            )
            messages.add_message(request, messages.INFO, "Ürün başarıyla oluşturulmuştur!")

            return redirect('/item_view')
        else:
            return render(request, "stocks/add_item.html", (context | {'error': new_item}))
    else:
        return render(request, "stocks/add_item.html", context)


@user_passes_test(lambda u: u.auth_level >= 2)
def edit_item(request, item_id) -> HttpResponse:
    item = Item.objects.get(ID=item_id)
    categories = Category.objects.order_by('-category')
    context = {
        'categories': categories,
        'item': item
    }
    if request.method == "POST":
        messages.add_message(request, messages.SUCCESS, "Ürün başarıyla düzenlenmiştir!")
        return redirect("stock_control:item_view")
    else:
        return render(request, "stocks/edit_item.html", context)

def item_details(request, item_id) -> HttpResponse:
    ...
@user_passes_test(lambda u: u.auth_level >= 2)
def delete_item(request, item_id) -> HttpResponse:
    item = Item.objects.get(ID=item_id)
    item.delete()
    messages.add_message(request, messages.WARNING, "Ürün başarıyla silinmiştir!")
    return redirect("stock_control:item_view")


@user_passes_test(lambda u: u.auth_level >= 2)
def statistics(request: str) -> HttpResponse:

    transactions_by_index = Transaction.objects.order_by('-time')
    total_income, total_cost, total_earned = 0, 0, 0

    with open(os.path.join(settings.BASE_DIR, 'stocks/stats.json')) as stats_json:
        stats = json.load(stats_json)
        for tran in transactions_by_index:
            tran_earned = (tran.item.price * tran.item.quantity) - (tran.item.cost * tran.item.quantity)

            total_income += tran.item.price * tran.item.quantity
            total_cost += tran.item.cost * tran.item.quantity
            total_earned += tran_earned
            if tran_earned > stats['global_stats'][0]['highest_all']:
                pass
                #json.dump({'highest_all': tran_earned}, stats_json)

    context = {
        'income': total_income,
        'cost': total_cost,
        'earned': total_earned
    }

    return render(request, "stocks/statistics.html", context)
