# Generated by Django 4.0.5 on 2022-08-22 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_business_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='is_active',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
