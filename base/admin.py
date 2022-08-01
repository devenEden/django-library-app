from django.contrib import admin
from .models import Book, Role, Borrowed
# Register your models here.

admin.site.register(Book)
admin.site.register(Role)
admin.site.register(Borrowed)
