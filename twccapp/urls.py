# twccapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('news/', views.news, name='news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('faqs/', views.faqs, name='faqs'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('publications/', views.publications_list, name='publications_list'),
    path('publications/<int:pk>/', views.publication_detail, name='publication_detail'),
    path('gallery/', views.gallery_view, name='gallery'),
    
]