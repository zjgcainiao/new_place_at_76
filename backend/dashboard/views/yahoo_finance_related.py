from .base import render, JsonResponse

## 2024-01-18 a yahoo-finance-based-portfolio-view
# import yfinance as yf
# from requests import Session
# from requests_cache import CacheMixin, SQLiteCache,CachedSession
# from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
# from pyrate_limiter import Duration, RequestRate, Limiter
# class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
#     pass

# yf_session = CachedLimiterSession(
#     limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
#     bucket_class=MemoryQueueBucket,
#     backend=SQLiteCache("yfinance.cache"),
# )

# def track_stocks_performance(request):
#     # Define the list of stock symbols
#     stock_symbols = [ 'DRV',]

#     # Dictionary to store stock data
#     stocks_data = {}
#     stocks_data_hist={}
#     for symbol in stock_symbols:
#         # Fetch data for each stock
#         stock = yf.Ticker(symbol,session=yf_session)
#         hist = stock.history(period="5d",interval="1h")  # You can adjust the period as needed
        
#         # Extracting last day's data (or any specific data you need)
#         last_day_data = hist.tail(1)
        
#         # Store data in the dictionary
#         stocks_data[symbol] = {
#             'Close': last_day_data['Close'].item(),
#             'Volume': last_day_data['Volume'].item(),
#             'Datetime': last_day_data.index.strftime('%Y-%m-%d %H:%M:%S').item(),
#             # Add more fields as needed
#         }

#         # Store historical data
#         stocks_data_hist[symbol] = {
#             # Convert 'Close' and 'Volume' series to lists for JSON serialization
#             'Close': hist['Close'].tolist(),
#             'Volume': hist['Volume'].tolist(),
#             'Datetime': hist.index.strftime('%Y-%m-%d %H:%M:%S').tolist(),
#             # Add more fields as needed
#         }
#     # Return data as JSON
#     return JsonResponse({'last_day_data': stocks_data, 'historical_data': stocks_data_hist})


# def get_stock_dash(request):
#     return render(request, 'dashboard/90_stock_dash.html')