# Generated by Django 4.0 on 2022-01-09 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_tweetrecord_id_alter_tweetrecord_tweet_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetrecord',
            name='tweet_id',
            field=models.CharField(default='1', max_length=100, primary_key=True, serialize=False),
        ),
    ]
