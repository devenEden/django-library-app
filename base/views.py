from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .forms import BookForm
from .models import Book


# Create your views here.
# login views

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login')
def home(request):
    total_books = Book.objects.count()
    books = Book.objects.all()
    context = {'books': books, 'total_books': total_books}
    return render(request, 'dashboard.html', context)


@login_required(login_url='/login')
def createBook(request):
    form = BookForm
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'books/books_form.html')
