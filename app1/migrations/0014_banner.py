# Generated by Django 3.2.12 on 2023-11-12 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_profile_wallet_bal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('description', models.CharField(max_length=100)),
            ],
        ),
    ]
