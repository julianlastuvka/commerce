# Generated by Django 3.2.9 on 2021-11-21 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing_watched_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='current_price',
            field=models.IntegerField(blank=True, default=models.IntegerField()),
        ),
    ]
