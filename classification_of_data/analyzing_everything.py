import sqlite3
import pandas as pd


def analyzing_sales(start_date=None, end_date=None):
    """
    Анализ продаж, заказов, остатков и возвратов.
    """
    db_file = '../classification_of_data/wildberries.db'
    conn = sqlite3.connect(db_file)
    query = "SELECT * FROM wildberries_data;"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df is None or df.empty: return None
    if 'date' not in df.columns: return None

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    if start_date and end_date:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    df['day'] = df['date'].dt.date
    df['week'] = df['date'].dt.isocalendar().week
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    df = df[df['isCancel'] == 0]

    # Анализ по городам и странам
    orders_by_city = df['warehouseName'].value_counts().reset_index()
    orders_by_city.columns = ['warehouseName', 'order_count']
    orders_by_country = df['countryName'].value_counts().reset_index()
    orders_by_country.columns = ['countryName', 'order_count']

    prices_by_city = df.groupby('warehouseName')['finishedPrice'].agg(['sum', 'mean']).reset_index()
    prices_by_city.columns = ['warehouseName', 'total_revenue', 'average_price']
    prices_by_country = df.groupby('countryName')['finishedPrice'].agg(['sum', 'mean']).reset_index()
    prices_by_country.columns = ['countryName', 'total_revenue', 'average_price']

    city_country_orders = df.groupby(['warehouseName', 'countryName']).size().reset_index(name='order_count')

    return {
        'orders_by_city': orders_by_city,
        'orders_by_country': orders_by_country,
        'prices_by_city': prices_by_city,
        'prices_by_country': prices_by_country,
        'city_country_orders': city_country_orders,
        'sales_data': df
    }


def analyzing_stocks():
    """
    Анализ остатков.
    """
    db_file = '../classification_of_data/wildberries.db'
    conn = sqlite3.connect(db_file)
    query = "SELECT * FROM wildberries_data;"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df is None or df.empty: return None

    stocks_by_city = df.groupby('warehouseName')['quantity'].sum().reset_index()
    stocks_by_city.columns = ['warehouseName', 'total_stock']

    return {
        'stocks_by_city': stocks_by_city,
        'stocks_data': df
    }
