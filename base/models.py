from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    updated = models.DateField(auto_now=True)
    updated = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Role(models.Model):
    role = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateField(auto_now=True)
    updated = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.role

#Book Requests
class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Returned', 'Returned'),
    )
    book_name = models.ForeignKey(Book, null=True, on_delete = models.SET_NULL)
    date_borrowed = models.DateTimeField(auto_now_add=False, auto_now= False, blank= True)
    return_date = models.DateTimeField(auto_now_add=False, auto_now= False, blank= True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    student_name = models.ForeignKey(Role, null=True, on_delete = models.SET_NULL)

    def __unicode__(self):
        return self.book_name
 