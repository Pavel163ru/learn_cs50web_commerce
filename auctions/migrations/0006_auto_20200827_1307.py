# Generated by Django 3.1 on 2020-08-27 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]