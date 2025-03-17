import sqlite3
import pandas as pd
import requests
from datetime import datetime, timedelta
import time
from settings.config import API_KEY
from url_queries.url import BASIC_URL


def get_wb_data(api_key, in_request, start_data, end_data, flag=0, **additional_filters):
    """
    Выполняет запрос к API Wildberries.
    """
    url = in_request['url']
    params_url = in_request['params_template'].copy()
    params_url['dateFrom'] = start_data

    if 'dateTo' in params_url: params_url['dateTo'] = end_data
    if 'flag' in params_url: params_url['flag'] = flag

    params_url.update(additional_filters)
    headers = {'Authorization': api_key}

    max_retries = 3  # Максимальное количество попыток
    retry_delay = 5  # Задержка между попытками (в секундах)

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ChunkedEncodingError: time.sleep(retry_delay)
        except requests.exceptions.RequestException: return None

    return None


def filter_data(data, **filter_param):
    """
    Фильтрует данные по заданным параметрам.
    """
    return [item for item in data if all(item.get(k) == v for k, v in filter_param.items())]


def create_table(db_file='wildberries.db', table_name='wildberries_data'):
    """
    Создает таблицу с уникальным ключом, если она не существует.
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                date TEXT,
                barcode TEXT,
                orderType TEXT,
                countryName TEXT,
                oblastOkrugName TEXT,
                regionName TEXT,
                category TEXT,
                subject TEXT,
                brand TEXT,
                finishedPrice TEXT,
                PRIMARY KEY (date, barcode, orderType)
            );
        """)


def remove_duplicates(db_file='wildberries.db', table_name='wildberries_data'):
    """
    Удаляет дубликаты из таблицы.
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            DELETE FROM {table_name}
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM {table_name}
                GROUP BY date, barcode, orderType
            );
        """)


def save_to_sqlite(data, db_file='wildberries.db', table_name='wildberries_data'):
    """
    Сохраняет данные в SQLite, избегая дублирования.
    """
    if not data: return None

    df = pd.DataFrame(data)

    while True:
        try:
            with sqlite3.connect(db_file) as conn:
                conn.execute("PRAGMA busy_timeout = 5000")
                cursor = conn.cursor()

                for _, row in df.iterrows():
                    # Проверяем, есть ли поле 'date' в данных
                    if 'date' not in row: continue

                    # Проверяем, существует ли запись
                    cursor.execute(f"""
                        SELECT 1 FROM {table_name}
                        WHERE date = ? AND barcode = ? AND orderType = ?
                    """, (row['date'], row['barcode'], row['orderType']))

                    if not cursor.fetchone():
                        # Если запись не существует, вставляем её
                        df_row = pd.DataFrame([row])
                        df_row.to_sql(table_name, conn, if_exists='append', index=False)
            break
        except sqlite3.OperationalError: time.sleep(1)


def update_sqlite(api_key, basic_url, db_file='wildberries.db', table_name='wildberries_data'):
    """
    Загружает данные из API, обновляет структуру таблицы и сохраняет их в базу данных SQLite.
    """
    end_data = datetime.now().strftime('%Y-%m-%d')
    start_data = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    # Проверяем, что даты не будущие
    if start_data > end_data: return

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        for name, in_request in basic_url.items():
            # Проверяем, поддерживает ли эндпоинт параметр orderType
            if 'orderType' in in_request['params_template']:
                data = get_wb_data(api_key, in_request, start_data, end_data, orderType='Клиентский')
            else:
                data = get_wb_data(api_key, in_request, start_data, end_data)

            if not data: continue

            df = pd.DataFrame(data)
            cursor.execute(f"PRAGMA table_info({table_name});")
            existing_columns = {column[1] for column in cursor.fetchall()}

            for column in df.columns:
                if column not in existing_columns:
                    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column} TEXT;")

            save_to_sqlite(data, db_file, table_name)

    # Удаляем дубликаты после обновления данных
    remove_duplicates(db_file, table_name)


def run_scheduler(api_key, basic_url):
    """
    Запускает планировщик для обновления данных каждый час.
    """
    create_table()  # Создаем таблицу, если она не существует
    update_sqlite(api_key, basic_url)


def data_param(start_data, end_data, **filter_param):
    """
    Главная функция для получения, фильтрации и сохранения данных.
    """
    all_data = []

    for name, in_request in BASIC_URL.items():
        if 'orderType' in in_request['params_template']:
            data = get_wb_data(API_KEY, in_request, start_data, end_data, orderType='Клиентский')
        else:
            data = get_wb_data(API_KEY, in_request, start_data, end_data)

        if data: all_data.extend(filter_data(data, **filter_param))

    if all_data: save_to_sqlite(all_data)


if __name__ == "__main__":
    create_table()
    remove_duplicates()

    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    filter_params = {'orderType': 'Клиентский'}

    data_param(start_date, end_date, **filter_params)

    run_scheduler(API_KEY, BASIC_URL)
