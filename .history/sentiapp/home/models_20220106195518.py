from django.db import models

# Create your models here.
from django.db import models
from django.db.models.fields import CharField, DateTimeField


class StockSummary(models.Model):

    ticker  =  CharField(max_length=200)
    last_fetched  =  DateTimeField("last_fetched", null=True)

    def __str__(self) -> str:
        return self.ticker






class StockRecords(models.Model):
