# Generated by Django 4.2.1 on 2023-06-03 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specimens', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specimensighting',
            name='image',
            field=models.TextField(verbose_name='изображение'),
        ),
    ]
