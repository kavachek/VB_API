from settings.config import API_KEY
from url_queries.url import BASIC_URL
from datetime import datetime, timedelta
from classification_of_data.collecting_information import get_wb_data, filter_data, save_to_sqlite, run_scheduler


def data_param(start_date, end_date, **filter_params):
    """
    Главная функция для получения, фильтрации и сохранения данных.
    """
    all_data = []

    for name, in_request in BASIC_URL.items():
        data = get_wb_data(API_KEY, in_request, start_date, end_date, **filter_params)

        if data:
            all_data.extend(filter_data(data, **filter_params))

    if all_data:
        save_to_sqlite(all_data)


if __name__ == "__main__":
    date_to = datetime.now().strftime('%Y-%m-%d')
    date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    filters = {'orderType': 'Клиентский'}
    data_param(date_from, date_to, **filters)

    # Запуск планировщика обновления данных
    run_scheduler(API_KEY, BASIC_URL)
