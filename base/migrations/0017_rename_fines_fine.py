# Generated by Django 4.0.5 on 2022-08-19 07:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0016_fines'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Fines',
            new_name='Fine',
        ),
    ]
