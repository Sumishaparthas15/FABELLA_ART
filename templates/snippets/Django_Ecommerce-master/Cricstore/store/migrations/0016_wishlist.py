# Generated by Django 4.2.5 on 2023-10-04 05:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_alter_sub_category_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wishtitle', models.CharField(max_length=250, unique=True)),
                ('wish', models.CharField(max_length=1000)),
                ('link', models.CharField(max_length=1000)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('is_achieved', models.BooleanField(blank=True, default=False)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
