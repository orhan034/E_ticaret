# Generated by Django 4.1.5 on 2023-03-01 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appMy', '0003_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date_now',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Tarih'),
        ),
    ]