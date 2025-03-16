import sqlite3

def get_last_date_from_db(db_path="wildberries.db", table_name="wildberries_data", date_column='date'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = f"SELECT MAX({date_column}) FROM {table_name}"
    cursor.execute(query)

    # Получаем результат
    last_date = cursor.fetchone()[0]
    conn.close()

    return last_date

last_date_in_bd = get_last_date_from_db()

if last_date_in_bd:
    print(f"Последняя дата из базы данных: {last_date_in_bd}")
else:
    print("Нет данных в базе.")
