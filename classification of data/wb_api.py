from settings.config import API_KEY
from url_queries.url import BASIC_URL
from start_algorithm.collecting_information import get_wb_data, filter_data, save_to_excel


def main(start_date, end_date, **filter_params):
    """
    Главная функция для получения, фильтрации и сохранения данных.

    :param start_date: Дата начала периода.
    :param end_date: Дата конца периода.
    :param filter_params: Дополнительные фильтры.
    """
    all_data = []

    # Получаем данные для каждого запроса
    for name, in_request in BASIC_URL.items():
        # Выполняем запрос к API
        data = get_wb_data(API_KEY, in_request, start_date, end_date, **filter_params)

        # Если данные получены, фильтруем их
        if data:
            filtered_data = filter_data(data, **filter_params)
            all_data.extend(filtered_data)
        else:
            continue

    # Сохраняем все данные в один файл
    if all_data:
        save_to_excel(all_data, 'wildberries_data.xlsx')

# Глобальные переменные
date_from = '2024-09-15'
date_to = '2024-09-15'
filters = {'orderType': 'Клиентский'}

main(date_from, date_to, **filters)
