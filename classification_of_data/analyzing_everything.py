import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def analyzing_sales():
    """
    Анализ продаж, заказов, остатков и возвратов с визуализацией и уведомлениями.
    """
    conn = sqlite3.connect('wildberries.db')
    query = f"SELECT * FROM {'wildberries_data'};"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Две проверки на подключение и проверки столбца 'date'
    if df is None or df.empty: return None
    if 'date' not in df.columns: return None

    # Преобразование даты в формат datetime
    df['date'] = pd.to_datetime(df['date'])

    # 1. Анализ продаж
    # Динамика продаж по дням, неделям, месяцам
    df['day'] = df['date'].dt.date
    df['week'] = df['date'].dt.isocalendar().week
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    # Фильтрация данных: оставляем только заказы, которые не были отменены (isCancel = 0)
    df = df[df['isCancel'] == 0]

    # 1. Анализ заказов по городам (warehouseName)
    orders_by_city = df['warehouseName'].value_counts().reset_index()
    orders_by_city.columns = ['warehouseName', 'order_count']

    # 2. Анализ заказов по странам (countryName)
    orders_by_country = df['countryName'].value_counts().reset_index()
    orders_by_country.columns = ['countryName', 'order_count']

    # 3. Анализ цен по городам
    prices_by_city = df.groupby('warehouseName')['finishedPrice'].agg(['sum', 'mean']).reset_index()
    prices_by_city.columns = ['warehouseName', 'total_revenue', 'average_price']

    # 4. Анализ цен по странам
    prices_by_country = df.groupby('countryName')['finishedPrice'].agg(['sum', 'mean']).reset_index()
    prices_by_country.columns = ['countryName', 'total_revenue', 'average_price']

    # 5. Соотношение заказов по городам и странам
    city_country_orders = df.groupby(['warehouseName', 'countryName']).size().reset_index(name='order_count')

    # Визуализация данных
    plt.figure(figsize=(18, 12))

    # График заказов по городам
    plt.subplot(3, 2, 1)
    sns.barplot(x='order_count', y='warehouseName', data=orders_by_city, palette='viridis')
    plt.title('Топ городов по количеству заказов (без отмен)')
    plt.xlabel('Количество заказов')
    plt.ylabel('Город')

    # График заказов по странам
    plt.subplot(3, 2, 2)
    sns.barplot(x='order_count', y='countryName', data=orders_by_country, palette='magma')
    plt.title('Топ стран по количеству заказов (без отмен)')
    plt.xlabel('Количество заказов')
    plt.ylabel('Страна')

    # График общей выручки по городам
    plt.subplot(3, 2, 3)
    sns.barplot(x='total_revenue', y='warehouseName', data=prices_by_city, palette='plasma')
    plt.title('Общая выручка по городам (без отмен)')
    plt.xlabel('Общая выручка')
    plt.ylabel('Город')

    # График средней цены по городам
    plt.subplot(3, 2, 4)
    sns.barplot(x='average_price', y='warehouseName', data=prices_by_city, palette='coolwarm')
    plt.title('Средняя цена заказа по городам (без отмен)')
    plt.xlabel('Средняя цена')
    plt.ylabel('Город')

    # График общей выручки по странам
    plt.subplot(3, 2, 5)
    sns.barplot(x='total_revenue', y='countryName', data=prices_by_country, palette='inferno')
    plt.title('Общая выручка по странам (без отмен)')
    plt.xlabel('Общая выручка')
    plt.ylabel('Страна')

    # График средней цены по странам
    plt.subplot(3, 2, 6)
    sns.barplot(x='average_price', y='countryName', data=prices_by_country, palette='cividis')
    plt.title('Средняя цена заказа по странам (без отмен)')
    plt.xlabel('Средняя цена')
    plt.ylabel('Страна')

    plt.tight_layout()
    plt.show()

    return {
        'orders_by_city': orders_by_city,
        'orders_by_country': orders_by_country,
        'prices_by_city': prices_by_city,
        'prices_by_country': prices_by_country,
        'city_country_orders': city_country_orders,
    }

analyzing_sales()