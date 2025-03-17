import sqlite3
import csv
import os
from datetime import datetime
import locale

BASE_CSV_FILE = "wildberries_report"

locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

# Подключаемся к БД
conn = sqlite3.connect(os.path.realpath('../classification_of_data/wildberries.db'))
cursor = conn.cursor()

# Запрос к БД: получаем все данные, сортируя по дате и времени (новые сверху)
query = """
    SELECT 
        date, countryName, oblastOkrugName, regionName, barcode, 
        category, subject, brand, finishedPrice
    FROM wildberries_data
    ORDER BY date DESC, SUBSTR(date, 12, 8) DESC  
"""
cursor.execute(query)
rows = cursor.fetchall()

# Закрываем соединение с БД
conn.close()

# Преобразуем данные в удобный формат
data_by_year = {}
for row in rows:
    raw_date, country, oblast, region, barcode, category, subject, brand, price = row

    # Проверяем, что дата не NULL
    if raw_date:
        date = raw_date.split("T")[0]  # Берем только YYYY-MM-DD
        time = raw_date.split("T")[1]  # Берем время после T (HH:MM:SS)
    else:
        continue  # Пропускаем записи без даты

    # Используем английский формат даты для месяца и года
    year = datetime.strptime(date, "%Y-%m-%d").strftime("%Y")  # Год
    month_year = datetime.strptime(date, "%Y-%m-%d").strftime("%B %Y")  # Месяц и год на английском

    if year not in data_by_year:
        data_by_year[year] = {}

    if month_year not in data_by_year[year]:
        data_by_year[year][month_year] = set()  # Используем множество для уникальности

    # Добавляем запись в множество для исключения дубликатов
    data_by_year[year][month_year].add((date, time, country, oblast, region, barcode, category, subject, brand, price))

# Записываем в CSV для каждого года
for year, months in data_by_year.items():
    csv_file = f"{BASE_CSV_FILE}_{year}.csv"

    with open(csv_file, "w", newline="", encoding="utf-8-sig") as file:  # Используем utf-8-sig для правильной кодировки
        writer = csv.writer(file, delimiter=";")  # Добавляем разделитель ";"

        # Заголовки
        writer.writerow(["Месяц",
                         "Дата",
                         "Время",
                         "Страна",
                         "Область",
                         "Регион",
                         "Артикул",
                         "Категория",
                         "Тип товара",
                         "Бренд",
                         "Финальная цена"])

        # Проходим по месяцам
        for month, records in months.items():
            # Записываем месяц и год только один раз
            writer.writerow([month] + [""] * 9)  # Месяц в первой ячейке, остальное пусто

            # Сортируем записи внутри месяца по дате и времени
            sorted_records = sorted(records, key=lambda x: (x[0], x[1]))  # Сортировка по дате и времени

            # Записываем данные по каждой строке (без дубликатов)
            for record in sorted_records:
                date, time, country, oblast, region, barcode, category, subject, brand, price = record
                writer.writerow([month, date, time, country, oblast, region, barcode, category, subject, brand, price])

    print(f"✅ Data for {year} saved in {csv_file}. Check before uploading to Google Sheets!")