from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from dataclasses import field
from django.forms import ModelForm
from .models import Book, Role, Order


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["username"].widget.attrs.update({
        #     'required' : '',
        #     'name' : 'username',
        #     'id' : 'username',
        #     'type' : 'text',
        #     'class' : 'form-input',
        #     'placeholder' : 'Peter Wakholi',
        #     'maxlength' : '16',
        #     'minlength' : '6'
        # })

        # self.fields["email"].widget.attrs.update({
        #     'required' : '',
        #     'name' : 'email',
        #     'id' : 'email',
        #     'type' : 'email',
        #     'class' : 'form-input',
        #     'placeholder' : 'peterwakholi.1@gmail.com'
        # })

        # self.fields["password1"].widget.attrs.update({
        #     'required' : '',
        #     'name' : 'password1',
        #     'id' : 'password1',
        #     'type' : 'password',
        #     'class' : 'form-input',
        #     'placeholder' : 'Password',
        #     'maxlength' : '22',
        #     'minlength' : '8'
        # })

        # self.fields["password2"].widget.attrs.update({
        #     'required' : '',
        #     'name' : 'password2',
        #     'id' : 'password2',
        #     'type' : 'password',
        #     'class' : 'form-input',
        #     'placeholder' : 'Confirm password',
        #     'maxlength' : '22',
        #     'minlength' : '8'
        # })

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = '__all__'

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


