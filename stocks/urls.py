from django.urls import path
from . import views

app_name = 'stock_control'

urlpatterns = [
    path('', views.index, name='index'),
    path('item_view/', views.item_view, name="item_view"),
    path('item_view/delete_item/<int:item_id>', views.delete_item, name="delete_item"),
    path('item_view/add_item', views.add_item, name="add_item"),
    path('item_view/<str:item_name>', views.item_details, name="item_details"),
    path('shipments', views.shipments, name="shipments_view"),
    path('statistics', views.statistics, name="statistics_view"),
]
