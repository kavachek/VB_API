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
    Сохраняет данные в SQLite.
    """
    if not data: return None

    df = pd.DataFrame(data)
    with sqlite3.connect(db_file) as conn: df.to_sql(table_name, conn, if_exists='append', index=False)


def update_sqlite(api_key, basic_url, db_file='wildberries.db', table_name='wildberries_data'):
    """
    Загружает данные из API, обновляет структуру таблицы и сохраняет их в базу данных SQLite.
    """
    date_to = datetime.now().strftime('%Y-%m-%d')
    date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        for name, in_request in basic_url.items():
            print(f"Запрашиваем данные для {name}...")

            data = get_wb_data(api_key, in_request, date_from, date_to)
            if not data:
                print(f"❌ Данные для {name} не получены.")
                continue

            df = pd.DataFrame(data)

            # Проверяем существующие столбцы в таблице
            cursor.execute(f"PRAGMA table_info({table_name});")
            existing_columns = {column[1] for column in cursor.fetchall()}

            # Добавляем недостающие столбцы в базу
            for column in df.columns:
                if column not in existing_columns:
                    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column} TEXT;")
                    print(f"✅ Добавлен новый столбец: {column}")

            # Сохраняем данные
            df.to_sql(table_name, conn, if_exists='append', index=False)
            print(f"✅ Данные для {name} успешно сохранены.")

    print("🎉 Обновление базы завершено!")


def run_scheduler(api_key, basic_url):
    """
    Запускает планировщик для обновления данных каждый час.
    """
    update_sqlite(api_key, basic_url)
    schedule.every().hour.do(update_sqlite, api_key, basic_url)

    while True:
        schedule.run_pending()
        time.sleep(1)
