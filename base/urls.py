from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path("signup/", views.signup, name="signup"),
    path('', views.home, name='home'),
    path('books/create-book', views.createBook, name='create_book'),
    path('books/edit-book/<str:pk>/', views.editBook, name='edit_book'),
    path('books/delete-book/<str:pk>/', views.deleteBook, name='delete_book'),
    path('books/borrow-book/<str:pk>/', views.borrowBook, name='borrow_book'),
    path('books/create_order/', views.createOrder, name='create_order'),
    path('books/book_requests/', views.bookRequests, name='book_requests'),
    path('books/confirm_book/<str:pk>/', views.confirmBook, name='confirm_book'),
    path('books/deny_book/<str:pk>/', views.denyBook, name='deny_book'),
    path('books/return_book/<str:pk>/', views.returnBook, name='return_book'),
    path('fines/book_fines/', views.bookFines, name='book_fines'),
    path('fines/confirm_fine_payment/<str:pk>/',
         views.confirmFinePayment, name="confirm_fine_payment"),

    path("reset_password/", auth_views.PasswordResetView.as_view(
        template_name="auth/reset_password.html"), name="reset_password"),

    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(
        template_name="auth/password_sent.html"), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="auth/confirm_password.html"), name="password_reset_confirm"),

    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="auth/password_complete.html"), name="password_rest_complete"),
]
