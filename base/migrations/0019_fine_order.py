# Generated by Django 4.0.5 on 2022-08-19 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_fine_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='fine',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.order'),
        ),
    ]
