import os
from datetime import datetime
from classification_of_data.analyzing_everything import analyzing_sales, analyzing_stocks
from export_excel import export_sales_report, export_stocks_report
from export_to_excel.save_path import save_path


def get_date_range():
    while True:
        input_start_date_str = input("Введите начальную дату (ГГГГ-ММ-ДД): ")
        input_end_date_str = input("Введите конечную дату (ГГГГ-ММ-ДД): ")

        try:
            input_start_date = datetime.strptime(input_start_date_str, "%Y-%m-%d")
            input_end_date = datetime.strptime(input_end_date_str, "%Y-%m-%d")
            return input_start_date, input_end_date
        except ValueError:
            print("Неверный формат даты! Используйте формат ГГГГ-ММ-ДД.")


if __name__ == "__main__":
    start_date, end_date = get_date_range()
    save_path = save_path()

    os.makedirs(save_path, exist_ok=True)

    # Анализируем данные
    sales_results = analyzing_sales(start_date, end_date)
    stocks_results = analyzing_stocks()

    # Экспортируем каждый отчет отдельно
    export_sales_report(sales_results, save_path, start_date, end_date)
    export_stocks_report(stocks_results, save_path, start_date, end_date)
