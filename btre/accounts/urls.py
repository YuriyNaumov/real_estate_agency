from django.urls import path
from . import views

app_name = 'accounts' # registering a namespace 

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('vse_zayavki/',views.vse_zayavki, name='vse_zayvki'),

] 