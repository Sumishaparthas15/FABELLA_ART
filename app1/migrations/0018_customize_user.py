# Generated by Django 3.2.12 on 2023-11-13 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_remove_customize_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='customize',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app1.profile'),
            preserve_default=False,
        ),
    ]
