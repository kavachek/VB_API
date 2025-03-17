import sqlite3
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

# Настройки для Google Sheets API
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'wbapi-453920-a33f58229e25.json'
SPREADSHEET_NAME = 'Wildberries Отчет'

# Авторизация
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPES)
client = gspread.authorize(creds)

try:
    spreadsheet = client.create(SPREADSHEET_NAME)
except gspread.exceptions.APIError as e: spreadsheet = client.open(SPREADSHEET_NAME)

# Добавляем доступ для двух почт
def add_permissions(file_id_param, emails_param):
    drive_service = build('drive', 'v3', credentials=creds)
    for email in emails_param:
        permission = {
            'type': 'user',
            'role': 'writer',  # Редактор (reader — читатель, commenter — комментатор)
            'emailAddress': email,
        }
        drive_service.permissions().create(
            fileId=file_id_param,
            body=permission,
            fields='id',
            sendNotificationEmail=False  # Для отключения уведомлений
        ).execute()

file_id = spreadsheet.id

emails = ['kavachek47@gmail.com']  # 'ant115952522@gmail.com'
add_permissions(file_id, emails)

conn = sqlite3.connect(os.path.realpath('../classification_of_data/wildberries.db'))
cursor = conn.cursor()

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
        date = raw_date.split("T")[0]
        time_str = raw_date.split("T")[1]
    else: continue

    year = datetime.strptime(date, "%Y-%m-%d").strftime("%Y")
    month_year = datetime.strptime(date, "%Y-%m-%d").strftime("%B %Y")

    if year not in data_by_year: data_by_year[year] = {}

    if month_year not in data_by_year[year]: data_by_year[year][month_year] = set()

    data_by_year[year][month_year].add((date, time_str, country, oblast, region, barcode, category, subject, brand, price))

# Создаем листы в Google Таблице для каждого года
for year, months in data_by_year.items():
    try:
        worksheet = spreadsheet.add_worksheet(title=year, rows=10000, cols=20)
    except gspread.exceptions.APIError: worksheet = spreadsheet.worksheet(year)

    # Очищаем лист (если он уже существовал)
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

    # Проходим по месяцам
    for month, records in months.items():
        # Записываем месяц и год только один раз
        worksheet.append_row([month] + [""] * 9)

        # Сортируем записи внутри месяца по дате и времени
        sorted_records = sorted(records, key=lambda x: (x[0], x[1]))

        # Собираем все данные в один список
        all_data = []
        for record in sorted_records:
            date, time_str, country, oblast, region, barcode, category, subject, brand, price = record
            all_data.append([month, date, time_str, country, oblast, region, barcode, category, subject, brand, price])

        # Отправка всех данных одним запросом
        worksheet.append_rows(all_data)

try:
    default_sheet = spreadsheet.get_worksheet(0)
    if default_sheet.title == "Sheet1": spreadsheet.del_worksheet(default_sheet)
except gspread.exceptions.APIError: pass
