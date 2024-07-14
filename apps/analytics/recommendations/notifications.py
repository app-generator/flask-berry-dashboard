import pandas as pd

from datetime import datetime
import calendar

def getRecommendations(**kwargs):

    recommendations = {"highest hourly sales": "",
                       "most daily sales": "",
                       "most monthly sales": "",
                       "highest daily gain": "",
                       "largest daily loss": "",
                       "highest monthly gain": "",
                       "largest monthly loss": ""}


    # get data
    hourly_summary = pd.read_csv('apps/analytics/recommendations/hourly_summary.csv')

    hourly_summary['date_of_business'] = pd.to_datetime(hourly_summary['date_of_business'], format="%Y-%m-%d")


    '''Highest Hourly Sale (for this month)'''

    # filter data on only those client-sites where we have at least 24 hourly transactions in a day 
    # # (otherwise its more likely the revenue attributed to that hour is actually for the entire day)
    highest_hourly = hourly_summary[(hourly_summary.salesYear==datetime.now().year) & 
                                    (hourly_summary.salesMonth==datetime.now().month) &
                                    (hourly_summary.num_hrly_txns>=24)] \
                                .sort_values('max_revenue', ascending = False)

    # prepare notification
    realm_site = f'{highest_hourly['realm'].iloc[0]}-{highest_hourly['entity_id'].iloc[0]}'
    stream = str(highest_hourly['stream_id'].iloc[0])
    revenue = "£{:,.0f}".format(highest_hourly['max_revenue'].iloc[0])
    bus_date = highest_hourly['date_of_business'].iloc[0].strftime("%d-%b")

    message = realm_site + '-' + stream  + ' ' +  revenue + ' ' +  bus_date

    recommendations["highest hourly sales"] = message

    
    '''Daily Summary'''

    daily_summary = hourly_summary.groupby(by = ['realm','entity_id', 'date_of_business', 'salesDay',  'salesMonth', 'salesYear', ], as_index = False) \
                                .agg({'sum_revenue': 'sum'}).sort_values(['realm','entity_id', 'salesDay', 'salesMonth', 'salesYear'])


    '''Most Daily Sales (for this month)'''

    most_daily = daily_summary[(daily_summary.salesYear==datetime.now().year) & (daily_summary.salesMonth==datetime.now().month)] \
                                .sort_values('sum_revenue', ascending = False)

    # prepare notification
    realm_site = f'{most_daily['realm'].iloc[0]}-{most_daily['entity_id'].iloc[0]}'
    revenue = "£{:,.0f}".format(most_daily['sum_revenue'].iloc[0])
    bus_date = most_daily['date_of_business'].iloc[0].strftime("%d-%b")

    message = realm_site + ' ' +  revenue + ' ' +  bus_date
    
    recommendations["most daily sales"] = message

    '''Monthly Summary'''

    monthly_summary = daily_summary.groupby(by = ['realm','entity_id','salesMonth', 'salesYear', ], as_index = False) \
                                .agg({'sum_revenue': 'sum'}).sort_values(['realm','entity_id', 'salesMonth', 'salesYear'])



    '''Most Monthly Sales'''

    most_monthly = monthly_summary[(monthly_summary.salesYear==datetime.now().year) & (monthly_summary.salesMonth==datetime.now().month)] \
                                .sort_values('sum_revenue', ascending = False)

    # prepare notification
    realm_site = f'{most_monthly['realm'].iloc[0]}-{most_monthly['entity_id'].iloc[0]}'
    revenue = "£{:,.0f}".format(most_monthly['sum_revenue'].iloc[0])
    bus_month = datetime.now().strftime("%b-%y")

    message = realm_site + ' ' +  revenue + ' ' +  bus_month
    recommendations["most monthly sales"] = message


    '''Daily Delta Changes'''
    
    # first sort in date order
    daily_summary = daily_summary.sort_values(['realm','entity_id', 'date_of_business'])
    daily_summary['daily_delta'] = daily_summary['sum_revenue'].diff() # add difference column

    '''Largest Daily Gain'''
    highest_daily_delta = daily_summary[(daily_summary.salesYear==datetime.now().year) & (daily_summary.salesMonth==datetime.now().month)] \
                                .sort_values(['daily_delta'], ascending = False)


    # prepare notification
    realm_site = f'{highest_daily_delta['realm'].iloc[0]}-{highest_daily_delta['entity_id'].iloc[0]}'
    revenue = "£{:,.0f}".format(highest_daily_delta['sum_revenue'].iloc[0])
    bus_date = highest_daily_delta['date_of_business'].iloc[0].strftime("%d-%b")

    message = realm_site + ' ' +  revenue + ' ' +  bus_date
    recommendations["highest daily gain"] = message


    # prepare notification
    realm_site = f'{highest_daily_delta['realm'].iloc[-1]}-{highest_daily_delta['entity_id'].iloc[-1]}'
    revenue = "£{:,.0f}".format(highest_daily_delta['sum_revenue'].iloc[-1])
    bus_date = highest_daily_delta['date_of_business'].iloc[-1].strftime("%d-%b")

    '''Largest Daily Loss'''
    message = realm_site + ' ' +  revenue + ' ' +  bus_date
    recommendations["largest daily loss"] = message


    '''Monthly Delta Changes'''

    # first sort in date order
    monthly_summary = monthly_summary.sort_values(['realm','entity_id', 'salesYear', 'salesMonth'])
    monthly_summary['monthly_delta'] = monthly_summary['sum_revenue'].diff() # add difference column

    highest_monthly_delta = monthly_summary[(monthly_summary.salesYear==datetime.now().year) & (monthly_summary.salesMonth==datetime.now().month)] \
                                .sort_values(['monthly_delta'], ascending = False)
    
     # prepare notification
    realm_site = f'{highest_monthly_delta['realm'].iloc[0]}-{highest_monthly_delta['entity_id'].iloc[0]}'
    revenue = "£{:,.0f}".format(highest_monthly_delta['sum_revenue'].iloc[0])
    bus_month = datetime.now().strftime("%b-%y")

    '''Largest Monthly Gain'''
    message = realm_site + ' ' +  revenue + ' ' +  bus_month
    recommendations["highest monthly gain"] = message

     # prepare notification
    realm_site = f'{highest_monthly_delta['realm'].iloc[-1]}-{highest_monthly_delta['entity_id'].iloc[-1]}'
    revenue = "£{:,.0f}".format(highest_monthly_delta['sum_revenue'].iloc[-1])
    bus_month = datetime.now().strftime("%b-%y")

    '''Largest Monthly Loss'''
    message = realm_site + ' ' +  revenue + ' ' +  bus_month
    recommendations["largest monthly loss"] = message
    
    return recommendations

# debug

# getRecommendations()
