from django.db import models

# Create your models here.
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, DateTimeField, IntegerField


class StockSummary(models.Model):

    ticker  =  models.CharField(primary_key=True, max_length=200, unique=True )
    last_fetched  = models.DateTimeField("last_fetched", null=True)

    def __str__(self) -> str:
        return self.ticker






class TweetRecord(models.Model):
    stock = models.ForeignKey(StockSummary, on_delete=models.CASCADE)
    tweet_date =  models.DateTimeField("date_fetched", null=True)
    raw_text = models.CharField(max_length=1000)
    processed_text = models.CharField(max_length=1000)
    polarity = models.DecimalField(max_digits=20, decimal_places=6)
    sentiment  =  models.CharField(max_length=200)
    subjectivity =  models.DecimalField(max_digits=20, decimal_places=6)
    neg =  models.DecimalField(max_digits=20, decimal_places=3)
    neu =  models.DecimalField(max_digits=20, decimal_places=3)
    pos  = models.DecimalField(max_digits=20, decimal_places=3)
    compound  = models.DecimalField(max_digits=20, decimal_places=4)

    


