# Generated by Django 3.2.9 on 2021-12-08 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_highest_bidder'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='listing_comments', to='auctions.listing'),
            preserve_default=False,
        ),
    ]
