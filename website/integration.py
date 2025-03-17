import sqlite3
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Настройки для Google Sheets API
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'wbapi-453920-a33f58229e25.json'
SPREADSHEET_NAME = 'Wildberries Отчет'

# Авторизация
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPES)
client = gspread.authorize(creds)

try:
    spreadsheet = client.create(SPREADSHEET_NAME)
except gspread.exceptions.APIError: spreadsheet = client.open(SPREADSHEET_NAME)

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

conn.close()

data_by_year = {}
for row in rows:
    raw_date, country, oblast, region, barcode, category, subject, brand, price = row

    # Проверяем, что дата не NULL
    if raw_date:
        date = raw_date.split("T")[0]  # Берем только YYYY-MM-DD
        time = raw_date.split("T")[1]  # Берем время после T (HH:MM:SS)
    else: continue

    year = datetime.strptime(date, "%Y-%m-%d").strftime("%Y")
    month_year = datetime.strptime(date, "%Y-%m-%d").strftime("%B %Y")

    if year not in data_by_year:
        data_by_year[year] = {}

    if month_year not in data_by_year[year]:
        data_by_year[year][month_year] = set()

    # Добавляем запись в множество для исключения дубликатов
    data_by_year[year][month_year].add((date, time, country, oblast, region, barcode, category, subject, brand, price))

# Создаем листы в Google Таблице для каждого года
for year, months in data_by_year.items():
    try:
        worksheet = spreadsheet.add_worksheet(title=year, rows=10000, cols=20)
    except gspread.exceptions.APIError: worksheet = spreadsheet.worksheet(year)

    worksheet.clear()

    # Заголовки
    worksheet.append_row(["Месяц",
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

    for month, records in months.items():
        worksheet.append_row([month] + [""] * 9)

        # Сортируем записи внутри месяца по дате и времени
        sorted_records = sorted(records, key=lambda x: (x[0], x[1]))

        # Пакетная запись данных
        batch_size = 100
        batch = []

        for record in sorted_records:
            date, time, country, oblast, region, barcode, category, subject, brand, price = record
            batch.append([month, date, time, country, oblast, region, barcode, category, subject, brand, price])

            if len(batch) >= batch_size:
                worksheet.append_rows(batch)
                batch = []
        time.sleep(120)
        if batch: worksheet.append_rows(batch)

try:
    default_sheet = spreadsheet.get_worksheet(0)
    if default_sheet.title == "Sheet1":
        spreadsheet.del_worksheet(default_sheet)
except gspread.exceptions.APIError:
    pass

print(f"✅ Данные успешно перенесены в Google Таблицу: {SPREADSHEET_NAME}")