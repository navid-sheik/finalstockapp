
from django.test import Client, SimpleTestCase, TransactionTestCase

from django.urls import reverse





class TestApi(TransactionTestCase):
    def test_mining_tweets_sentiment(self):
        user = Client()
        response = user.get(reverse('home:start_mining_tweets', kwargs={'ticker_id':'TSLA'})) 
        self.assertEqual(response.status_code, 200)

    def test_get_list_stock(self):
        user = Client()
        response = user.get(reverse('home:get_all_mining_tweets')) 
        self.assertEqual(response.status_code, 200)
