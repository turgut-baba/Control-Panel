from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_user, name="login_url"),
    path('register/', views.register_view, name="register_url"),
    path('logout/', views.logout_user, name="logout_url"),
    path('vendors/', views.user_vendor, name="vendor_url"),
    path('vendors/add', views.add_vendor, name="add_vendor"),
    path('settings', views.panel_settings, name="panel_settings")
]
