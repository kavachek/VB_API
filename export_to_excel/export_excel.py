from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
import os

def export_to_excel_with_chart(analysis_results, save_path, filename="output.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Города и выручка"

    headers = ["Город", "Количество заказов", "Общая выручка", "Средняя цена"]
    ws.append(headers)

    orders_by_city = analysis_results['orders_by_city']
    prices_by_city = analysis_results['prices_by_city']
    merged_data = orders_by_city.merge(prices_by_city, on='warehouseName', how='left')

    for index, row in merged_data.iterrows():
        ws.append([row['warehouseName'], row['order_count'], row['total_revenue'], row['average_price']])

    chart = BarChart()
    chart.title = "Количество заказов по городам"
    chart.x_axis.title = "Город"
    chart.y_axis.title = "Количество заказов"

    data = Reference(ws, min_col=2, min_row=1, max_row=len(merged_data) + 1)
    categories = Reference(ws, min_col=1, min_row=2, max_row=len(merged_data) + 1)

    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)

    chart.width = 20
    chart.height = 10
    ws.add_chart(chart, "H2")

    full_path = os.path.join(save_path, filename)
    wb.save(full_path)
