from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .forms import BookForm
from .models import Book


# Create your views here.


def home(request):
    total_books = Book.objects.count();
    books = Book.objects.all()
    context = {'books': books, 'total_books': total_books}
    return render(request, 'dashboard.html', context)

def createBook(request):
    form = BookForm
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'books/books_form.html')

# login views
def loginPage(request):
    context = {
        'username': '',
        'password': ''
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
 
        context['username'] = username
        context['password'] = password
 
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Invalid Credentials')
 
        user = authenticate(request, username=username, password=password)
 
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong credentials')
 
    return render(request, 'auth/login.html', context)
