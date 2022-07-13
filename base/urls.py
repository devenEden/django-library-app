from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/edit-book/<str:pk>/', views.editBook, name='edit_book'),
    path('books/delete-book/<str:pk>/', views.deleteBook, name='delete_book'),
    path('books/create-book', views.createBook, name='create_book'),
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginPage, name='login'),
    path("signup/", views.signup, name="signup"),
]
