from django.db import models

# Create your models here.
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, DateTimeField, IntegerField


class StockSummary(models.Model):

    ticker  =  models.CharField(max_length=200)
    last_fetched  = models.DateTimeField("last_fetched", null=True)

    def __str__(self) -> str:
        return self.ticker






class TweetRecord(models.Model):
    tweet_date =  models.DateTimeField("date_fetched", null=True)
    raw_text = models.CharField(max_length=1000)
    processed_text = models.CharField(max_length=1000)
    polarity = models.IntegerField()
    sentiment  =  models.CharField(max_length=10)
    subjectivity =  models.IntegerField()
    neg =  models.IntegerField()

    neu =  models.IntegerField()

    pos  = models.IntegerField()
    compound  = models.IntegerField()

    


