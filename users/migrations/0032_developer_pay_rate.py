# Generated by Django 4.0.5 on 2022-09-21 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_rename_userprofile_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='pay_rate',
            field=models.BigIntegerField(null=True),
        ),
    ]
