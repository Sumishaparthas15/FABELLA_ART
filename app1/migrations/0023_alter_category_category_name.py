# Generated by Django 3.2.12 on 2023-11-22 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0022_alter_category_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
