from django.urls import path
from .views import client_list, client_detail, client_create, client_update, client_delete

urlpatterns = [
    path('', client_list, name='client_list'),
    path('<int:client_id>/', client_detail, name='client_detail'),
    path('create/', client_create, name='client_create'),
    path('edit/<int:client_id>/', client_update, name='client_update'),
    path('delete/<int:client_id>/', client_delete, name='client_delete'),
]
