from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/create-book', views.createBook, name='create_book'),
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginPage, name='login'),
    path("signup/", views.signup, name = "signup"),
]
