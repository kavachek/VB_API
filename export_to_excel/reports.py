from datetime import datetime
from classification_of_data.analyzing_everything import analyzing_sales
from export_excel import export_to_excel_with_chart
from export_to_excel.save_path import get_save_path

def get_date_range():
    while True:
        input_start_date = input("Введите начальную дату (ГГГГ-ММ-ДД): ")
        input_end_date = input("Введите конечную дату (ГГГГ-ММ-ДД): ")

        try:
            start_date = datetime.strptime(input_start_date, "%Y-%m-%d")
            end_date = datetime.strptime(input_end_date, "%Y-%m-%d")
            return None, start_date, end_date
        except ValueError:
            print("Неверный формат даты! Используйте формат ГГГГ-ММ-ДД.")

if __name__ == "__main__":
    error_message, start_date, end_date = get_date_range()
    # Путь к файлу
    save_path = get_save_path()

    # Анализируем данные
    analysis_results = analyzing_sales(start_date, end_date)

    if analysis_results: export_to_excel_with_chart(analysis_results, save_path, filename="cities_revenue.xlsx")
    else: print("Не удалось выполнить анализ. Возможно, данные по выбранным датам отсутствуют в базе данных.")
