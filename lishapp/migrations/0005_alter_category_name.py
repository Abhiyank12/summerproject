# Generated by Django 4.1.3 on 2023-04-10 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lishapp', '0004_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default=False, max_length=100, unique=True),
        ),
    ]
