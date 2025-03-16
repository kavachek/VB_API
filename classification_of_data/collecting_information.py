import sqlite3
import pandas as pd
import requests
from datetime import datetime, timedelta
import time
import schedule


def get_wb_data(api_key, in_request, date_from, date_to, flag=0, **filters):
    """
    Выполняет запрос к API Wildberries.
    """
    url = in_request['url']
    params_url = in_request['params_template'].copy()
    params_url['dateFrom'] = date_from

    if 'dateTo' in params_url: params_url['dateTo'] = date_to
    if 'flag' in params_url: params_url['flag'] = flag

    params_url.update(filters)
    headers = {'Authorization': api_key}

    try:
        response = requests.get(url, params=params_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException: return None


def filter_data(data, **filters):
    """
    Фильтрует данные по заданным параметрам.
    """
    return [item for item in data if all(item.get(k) == v for k, v in filters.items())]


def save_to_sqlite(data, db_file='wildberries.db', table_name='wildberries_data'):
    """
    Сохраняет данные в SQLite с блокировкой на время записи.
    """
    if not data: return None

    df = pd.DataFrame(data)

    while True:
        try:
            with sqlite3.connect(db_file) as conn:
                conn.execute("PRAGMA busy_timeout = 5000")
                df.to_sql(table_name, conn, if_exists='append', index=False)
            break
        except sqlite3.OperationalError as e:
            print(f"База данных заблокирована, повторная попытка через 1 секунду. Ошибка: {e}")
            time.sleep(1)


def update_sqlite(api_key, basic_url, db_file='wildberries.db', table_name='wildberries_data'):
    """
    Загружает данные из API, обновляет структуру таблицы и сохраняет их в базу данных SQLite.
    """
    date_to = datetime.now().strftime('%Y-%m-%d')
    date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        for name, in_request in basic_url.items():
            data = get_wb_data(api_key, in_request, date_from, date_to)

            if not data:
                continue

            df = pd.DataFrame(data)
            cursor.execute(f"PRAGMA table_info({table_name});")
            existing_columns = {column[1] for column in cursor.fetchall()}

            for column in df.columns:
                if column not in existing_columns:
                    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column} TEXT;")

            df.to_sql(table_name, conn, if_exists='append', index=False)


def run_scheduler(api_key, basic_url):
    """
    Запускает планировщик для обновления данных каждый час.
    """
    update_sqlite(api_key, basic_url)
    schedule.every().hour.do(update_sqlite, api_key, basic_url)

    while True:
        schedule.run_pending()
        time.sleep(1)
