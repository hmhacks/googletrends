from pytrends.request import TrendReq

# Only need to run this once, the rest of requests will use the same session.
pytrends = TrendReq()

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
# pytrend.build_payload(kw_list=['unemployment', 'robinhood'])

kw_list=['unemployment', 'robinhood']

# Interest Over Time
# interest_over_time_df = pytrend.interest_over_time()

df = pytrends.get_historical_interest(kw_list, year_start=2004, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)

# print(interest_over_time_df.head())
print(df.head())
