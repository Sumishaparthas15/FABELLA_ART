# Generated by Django 4.2.5 on 2023-09-12 21:23

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_additional_information_product_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='availability',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='featured_image',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='model_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='total_quantity',
            field=models.IntegerField(),
        ),
    ]
