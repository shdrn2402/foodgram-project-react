# Generated by Django 3.2.13 on 2023-03-18 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20220614_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=250, unique=True, verbose_name='Название ярлыка'),
        ),
    ]
