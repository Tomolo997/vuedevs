# Generated by Django 4.0.5 on 2022-08-30 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_alter_messagebusinesstodeveloper_receipter_id_developer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagebusinesstodeveloper',
            name='receipter_id_developer',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='messagebusinesstodeveloper',
            name='sender_id_business',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
