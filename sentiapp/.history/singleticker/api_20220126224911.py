



from django.http import JsonResponse
import requests



def fetchStockData( request,ticker_id):
    stock_ticker =  ticker_id.lower()
    url  =  f'https://cloud.iexapis.com/stable/stock/{ticker_id}/quote?token=pk_8295cd8fa9064272b2335b548a28d293'
    # url  =  f'https://cloud.iexapis.com/stable/stock/{stock_ticker}/chart/5d?token=pk_8295cd8fa9064272b2335b548a28d293'
   
    response =  requests.get(url).json()
    print(response)
    return JsonResponse({'stock_quote': response })
