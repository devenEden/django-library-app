# Generated by Django 4.0.5 on 2022-08-07 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_order_return_date_alter_order_date_borrowed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='book',
            new_name='book_name',
        ),
    ]
