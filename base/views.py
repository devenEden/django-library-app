from django.shortcuts import render, redirect

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
