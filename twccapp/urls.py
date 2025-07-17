# twccapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<int:pk>/', views.services_detail, name='services_detail'),
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
    path('gallery/<int:pk>/', views.gallery_detail, name='gallery_detail'),
    path('publications/<int:pk>/', views.publication_detail, name='publication_detail'),
    path('projects-programs/', views.projects_programs, name='projects_programs'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
   
]