import requests
import pandas as pd
import sqlite3


def get_wb_data(api_key, in_request, date_from, date_to, flag=0, **filters):
    """
    Выполняет запрос к API Wildberries.

    :param api_key: Ключ к API WB.
    :param in_request: Словарь с URL и шаблоном параметров.
    :param date_from: Дата начала периода (строка в формате 'YYYY-MM-DD').
    :param date_to: Дата конца периода (опционально, для некоторых запросов).
    :param flag: Флаг (0 или 1, опционально).
    :param filters: Дополнительные фильтры (например, статус заказа, артикул).
    :return: JSON-ответ или None в случае ошибки.
    """
    url = in_request['url']
    params_url = in_request['params_template'].copy() # Нужно для копирования всех параметров запроса

    params_url['dateFrom'] = date_from
    if 'dateTo' in params_url: params_url['dateTo'] = date_to
    if 'flag' in params_url: params_url['flag'] = flag

    # Добавление дополнительных фильтров
    params_url.update(filters)
    headers = {'Authorization': api_key}

    # Проверка, что есть подключение к API WB
    try:
        response = requests.get(url, params=params_url, headers=headers)
        response.raise_for_status() # Проверка на ошибки
        return response.json()
    except requests.exceptions.RequestException:
        return None


def filter_data(data, **filters):
    """
    Фильтрует данные по заданным параметрам.

    :param data: Данные в формате JSON.
    :param filters: Параметры фильтрации (например, статус заказа, артикул).
    :return: Отфильтрованные данные.
    """
    filtered_data = []
    for item in data:
        match = True
        for key, value in filters.items():
            if item.get(key) != value:
                match = False
                break
        if match:
            filtered_data.append(item)

    return filtered_data


def save_to_sqlite(data, db_file='wildberries.db', table_name='wildberries_data'):
    """
    Сохраняет данные в SQLite.

    :param data: Данные в формате JSON.
    :param db_file: Путь к файлу базы данных SQLite.
    :param table_name: Название таблицы в БД.
    """
    # Проверка, что данные есть
    if not data: return None

    # Создаем DataFrame из данных
    df = pd.DataFrame(data)
    conn = sqlite3.connect(db_file)

    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    finally:
        conn.close()
