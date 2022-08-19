from django.contrib import admin
from .models import Book, Fine, Role, Order
# Register your models here.

admin.site.register(Book)
admin.site.register(Role)
admin.site.register(Order)
admin.site.register(Fine)
