from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('list/', views.document_list, name='document_list'),
    path('forward/<int:pk>/', views.forward_document, name='forward_document'),
    path('<int:pk>/', views.document_detail, name='document_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
