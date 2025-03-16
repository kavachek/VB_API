import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from io import BytesIO
from classification_of_data.analyzing_everything import analyzing_sales


def export_to_excel_with_charts(analysis_results, filename="output.xlsx"):
    """
    Экспорт данных и графиков в Excel.

    :param analysis_results: Результаты анализа из analyzing_sales().
    :param filename: Имя файла для сохранения.
    """
    # Создаем Excel-файл
    wb = Workbook()
    ws = wb.active
    ws.title = "Города и выручка"

    # Добавляем заголовки
    headers = ["Город", "Количество заказов", "Общая выручка", "Средняя цена"]
    ws.append(headers)

    # Получаем данные из результатов анализа
    orders_by_city = analysis_results['orders_by_city']
    prices_by_city = analysis_results['prices_by_city']

    # Начальная позиция для вставки графиков
    img_row = 2  # Начинаем с 2 строки, так как 1 строка — заголовки

    # Обрабатываем каждый город
    for index, row in orders_by_city.iterrows():
        city = row['warehouseName']
        order_count = row['order_count']

        # Находим данные о выручке и средней цене для этого города
        city_revenue_data = prices_by_city[prices_by_city['warehouseName'] == city]
        total_revenue = city_revenue_data['total_revenue'].values[0]
        average_price = city_revenue_data['average_price'].values[0]

        # Добавляем данные в Excel
        ws.append([city, order_count, total_revenue, average_price])

        # Создаем график
        plt.figure(figsize=(6, 4))
        plt.bar(["Заказы", "Выручка", "Средняя цена"], [order_count, total_revenue, average_price],
                color=['blue', 'green', 'orange'])
        plt.title(f"Показатели для города: {city}")
        plt.ylabel("Значение")

        # Сохраняем график в буфер
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        plt.close()

        # Вставляем график в Excel
        img_buffer.seek(0)
        img = Image(img_buffer)
        img.anchor = f'E{img_row}'  # Вставляем график в столбец E
        ws.add_image(img)

        # Переходим к следующей строке
        img_row += 1

    # Сохраняем файл
    wb.save(filename)
    print(f"Файл {filename} успешно создан.")


if __name__ == "__main__":
    # Получаем результаты анализа из первого файла
    analysis_results = analyzing_sales()

    # Экспортируем данные в Excel
    if analysis_results:
        export_to_excel_with_charts(analysis_results, filename="cities_revenue.xlsx")