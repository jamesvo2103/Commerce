# Generated by Django 5.1.4 on 2024-12-29 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting_bid_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]