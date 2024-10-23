from django.urls import path
from . import views

urlpatterns = [
    path('', views.facture_list, name='facture_list'),
    path('client/<int:client_id>/', views.facture_list, name='factures_by_client'),
    path('<int:pk>/', views.facture_detail, name='facture_detail'),
    path('create/', views.facture_create, name='facture_create'),
    path('edit/<int:pk>/', views.facture_update, name='facture_update'),
    path('delete/<int:pk>/', views.facture_delete, name='facture_delete'),
]
