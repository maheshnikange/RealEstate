# Generated by Django 4.2.1 on 2023-06-04 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='activate_flag',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
