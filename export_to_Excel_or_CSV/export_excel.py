import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from io import BytesIO
from classification_of_data.analyzing_everything import analyzing_sales


def export_to_excel_with_charts(analysis_results, filename="output.xlsx"):
    """
    Экспорт данных и одного общего графика в Excel.

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

    # Объединяем данные в одну таблицу
    merged_data = orders_by_city.merge(prices_by_city, on='warehouseName', how='left')

    # Добавляем данные в Excel
    for index, row in merged_data.iterrows():
        city = row['warehouseName']
        order_count = row['order_count']
        total_revenue = row['total_revenue']
        average_price = row['average_price']
        ws.append([city, order_count, total_revenue, average_price])

    # Создаем общий график
    plt.figure(figsize=(10, 6))
    cities = merged_data['warehouseName']
    order_counts = merged_data['order_count']

    # График количества заказов
    plt.bar(cities, order_counts, color='blue', label='Количество заказов')

    plt.title('Показатели по городам')
    plt.xlabel('Город')
    plt.ylabel('Значение')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Сохраняем график в буфер
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()

    img_buffer.seek(0)
    img = Image(img_buffer)
    img.anchor = 'E2'
    ws.add_image(img)

    wb.save(filename)


if __name__ == "__main__":
    analysis = analyzing_sales()

    if analysis:
        export_to_excel_with_charts(analysis, filename="cities_revenue.xlsx")
