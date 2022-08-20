from datetime import datetime
from itertools import count
from telnetlib import STATUS
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from .forms import BookForm, OrderForm, RoleForm, SignUpForm
from .models import Book, Fine, Role, Order
from django.db.models import Q
from django.utils import timezone

# Create your views here.
# SIGNUP


def signup(request):
    form = SignUpForm()
    context = {
        'username': '',
        'password1': '',
        'password2': '',
        'email': '',
        'form': form
    }
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        context['username'] = request.POST.get('username')
        context['password1'] = request.POST.get('password1')
        context['password2'] = request.POST.get('password2')
        context['email'] = request.POST.get('email')
        context['form'] = form
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            form.save()
            new_user = authenticate(username=username, password=password)
            role = RoleForm({'user': new_user.id, 'role': 'Student'})
            role.save()
            if new_user is not None:
                login(request, new_user)
                return redirect("home")
        else:
            messages.error(request, form.errors)

    return render(request, "auth/signup.html", context)


# login views

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    total_students = Role.objects.filter(role='Student').count()
    total_books = Book.objects.count()
    books = Book.objects.filter(Q(title__icontains=q) | Q(author__icontains=q))
    user_role = Role.objects.get(user=request.user.id)
    total_fines = Fine.objects.filter(status='Not Paid').count()

    context = {
        'books': books,
        'total_books': total_books,
        'total_students': total_students,
        'user_role': user_role,
        'q': q,
        "total_fines": total_fines
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='/login')
def createBook(request):
    form = BookForm
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            messages.success(request, "Book has been created")
            form.save()
            return redirect('home')
    return render(request, 'books/books_form.html')

# edit book view


@login_required(login_url='/login')
def editBook(request, pk):
    book = Book.objects.get(id=pk)
    context = {
        'book': book
    }

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            messages.success(request, "Book has been edited")
            form.save()
            return redirect('home')
    return render(request, 'books/edit_book_form.html', context)


@login_required(login_url='/login')
def deleteBook(request, pk):
    book = Book.objects.get(id=pk)
    context = {
        'book': book
    }
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book has been deleted")
        return redirect('home')
    return render(request, 'books/delete_book.html', context)
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

# Book_requests


@login_required(login_url='/login')
def borrowBook(request, pk):
    book = Book.objects.get(id=pk)
    borrowed_book = True
    has_fine = False
    orders = Order.objects.filter(
        Q(status="Accepted") | Q(status="Pending"),
        book_name=book.id
    ).count()

    previous_fine = Fine.objects.filter(
        student_name=request.user,
        book_name=book.id,
        status="Not Paid"
    ).count()

    if previous_fine > 0:
        has_fine = True

    if orders >= 1:
        borrowed_book = False

    context = {
        'book': book,
        "borrowed_book": borrowed_book,
        "has_fine": has_fine
    }

    if request.method == 'POST':
        return redirect('book_requests')
    return render(request, 'books/borrow_book.html', context)


@login_required(login_url='/login')
def createOrder(request):
    form = OrderForm()
    book_name = request.POST.get("book_name")
    if request.method == 'POST':
        form = OrderForm(
            {
                "status": "Pending",
                "date_borrowed": datetime.now(),
                "book_name": book_name,
                "return_date": datetime.now(),
                "student_name": request.user
            })
        if form.is_valid():
            form.save()
            return redirect('book_requests')
        else:
            print(form.errors)

    return redirect('book_requests')


@login_required(login_url='/login')
def bookRequests(request):
    total_orders = Order.objects.filter(
        status='Pending',
        student_name=request.user
    )
    total_orders_admin = Order.objects.filter(status='Pending')
    borrowed_books = Order.objects.filter(status="Accepted")
    user_role = Role.objects.get(user=request.user.id)
    total_books = Book.objects.count()
    current_book_borrowed = Order.objects.filter(
        student_name=request.user).order_by("-id")[:1]
    all_requests = Order.objects.all().order_by("-id")

    current = {}
    return_warn_message = ""

    if len(current_book_borrowed) > 0:
        current = current_book_borrowed[0]
        return_date = str(current.return_date).split(" ")
        now = str(datetime.now()).split(" ")
        return_date = datetime.strptime(return_date[0], '%Y-%m-%d')
        now = datetime.strptime(now[0], '%Y-%m-%d')
        diff = (now-return_date).days

        if diff >= 3 and current.status == "Accepted":
            return_warn_message = "You have been fined 5000 for exceeding the return date by 3 days"
        if diff >= 10:
            return_warn_message = "You have been fined 15000 for exceeding the return date by 10 days"
        elif diff < 1 and abs(diff) <= 3:
            return_warn_message = "You have " + \
                str(abs(diff)) + \
                " day(s) until the return date"
        elif abs(diff) < 3 and current.status == "Accepted":
            return_warn_message = "You have " + \
                str(abs(diff)) + \
                " day(s) to return this book or you will be fined. Note that you have exceeded the return date"

    else:
        current["status"] = "Returned"

    context = {
        'total_order_count': len(total_orders_admin),
        'total_orders': total_orders,
        'total_borrowed': len(borrowed_books),
        'user_role': user_role,
        'borrowed_books': borrowed_books,
        'total_books': total_books,
        "total_orders_admin": total_orders_admin,
        "current_book_borrowed": current,
        "return_warn_message": return_warn_message,
        "all_requests": all_requests
    }

    return render(request, "books/book_requests.html", context)


def confirmBook(request, pk):
    order = Order.objects.get(id=pk)
    inputs = {"return_date": "", "date_borrowed": ""}
    if request.method == 'POST':
        form = OrderForm({
            "status": "Accepted",
            "date_borrowed": request.POST.get("date_borrowed"),
            "book_name": order.book_name,
            "return_date": request.POST.get("return_date"),
            "student_name": order.student_name,
        }, instance=order)
        inputs["return_date"] = request.POST.get("return_date")
        inputs["date_borrowed"] = request.POST.get("date_borrowed")
        if form.is_valid():
            form.save()
            messages.success(request, "Book has been issued")
            return redirect('book_requests')
        else:
            print(form.errors)

    context = {
        "order": order,
        "form": inputs
    }
    return render(request, 'books/confirm_book_form.html', context)


@login_required(login_url="/login")
def denyBook(request, pk):
    order = Order.objects.get(id=pk)
    context = {}
    if request.method == 'POST':
        order.delete()
        return redirect('book_requests')
    return render(request, 'books/deny_book.html', context)


@login_required(login_url="/login")
def returnBook(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        return_date = str(order.return_date).split(" ")
        now = str(datetime.now()).split(" ")
        return_date = datetime.strptime(return_date[0], '%Y-%m-%d')
        now = datetime.strptime(now[0], '%Y-%m-%d')
        diff = (now-return_date).days

        previous_fine = Fine.objects.filter(
            student_name=order.student_name,
            book_name=order.book_name,
            status="Not Paid"
        ).count()

        fine_amount = 5000

        if diff > 9:
            fine_amount = 15000

        fine = Fine(
            student_name=order.student_name,
            book_name=order.book_name,
            fine=fine_amount,
            status="Not Paid",
            return_date=order.return_date,
            order=order,
            payment_date=timezone.now()
        )

        fine_message = "Fine for " + \
            str(order.student_name) + " for " + \
            str(order.book_name) + " Book " + \
            ". Amount to be paid is UGX " + str(fine_amount)
        if previous_fine == 0 and diff >= 3:
            fine.save()
            messages.info(request, fine_message)
            return redirect("book_fines")
        if previous_fine > 0 and diff >= 10:
            fine = Fine.objects.get(
                student_name=order.student_name,
                book_name=order.book_name,
                status="Not Paid")
            fine.fine = 15000
            fine.save()
            messages.info(request, fine_message)
            return redirect("book_fines")
        if previous_fine > 0 and diff >= 3:
            messages.info(request, fine_message)
            return redirect("book_fines")
        elif diff < 3:
            order.status = "Returned"
            order.save()
            messages.info(request, "Book has been returned")

    return redirect('book_requests')


# Fines

@login_required(login_url="/login")
def bookFines(request):
    fine_history = []
    current_fine = {}
    total_fines_unpaid = 0
    total_fines_paid = 0
    students_with_fines = 0
    user_role = Role.objects.get(user=request.user.id)
    try:
        current_fine = Fine.objects.filter(
            student_name=request.user).order_by("-id")[:1]
        current_fine = current_fine[0]
        fine_history = Fine.objects.filter(student_name=request.user)

    except:
        pass

    total_fines = Fine.objects.all().order_by("-status")

    for fine in total_fines:
        students_with_fines = students_with_fines + 1
        if fine.status == "Paid":
            total_fines_paid += fine.fine
        else:
            total_fines_unpaid += fine.fine

    context = {
        "current_fine": current_fine,
        "fine_history": fine_history,
        "total_fines_paid": total_fines_paid,
        "total_fines_unpaid": total_fines_unpaid,
        "students_with_fines": students_with_fines,
        "total_fines": total_fines,
        "user_role": user_role
    }

    return render(request, 'fines/book_fines.html', context)


def confirmFinePayment(request, pk):
    if request.method == "POST":
        fine = Fine.objects.get(id=pk)
        fine.status = "Paid"
        fine.payment_date = timezone.now()
        order = Order.objects.get(id=fine.order.id)
        fine.save()
        order.status = "Returned"
        order.save()
        messages.info(
            request, "Fine has been paid and the book has been returned")

    return redirect("book_fines")
