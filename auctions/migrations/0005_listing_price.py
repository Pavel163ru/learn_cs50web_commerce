# Generated by Django 3.1 on 2020-08-27 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
