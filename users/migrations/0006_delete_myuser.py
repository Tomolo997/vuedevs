# Generated by Django 4.0.5 on 2022-07-14 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_myuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
