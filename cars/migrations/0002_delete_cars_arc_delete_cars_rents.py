# Generated by Django 4.1.2 on 2022-10-09 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cars_ARC',
        ),
        migrations.DeleteModel(
            name='Cars_Rents',
        ),
    ]
