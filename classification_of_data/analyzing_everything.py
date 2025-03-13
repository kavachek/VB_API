import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def fetch_data_from_db(db_file='wildberries.db', table_name='wildberries_data'):
    """
    Извлекает данные из SQLite-базы данных.

    :param db_file: Путь к файлу базы данных.
    :param table_name: Название таблицы.
    :return: DataFrame с данными.
    """
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect(db_file)

        # Читаем данные в DataFrame
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, conn)

        # Закрываем соединение
        conn.close()

        return df
    except Exception as e:
        print(f"Ошибка при чтении данных из базы данных: {e}")
        return None


def send_notification(message):
    """
    Отправляет уведомление (в данном случае просто выводит в консоль).

    :param message: Текст уведомления.
    """
    print(f"Уведомление: {message}")


def analyzing_sales():
    """
    Анализ продаж, заказов, остатков и возвратов с визуализацией и уведомлениями.
    """
    # Чтение данных из базы данных
    df = fetch_data_from_db()

    if df is None or df.empty:
        print("Ошибка: Не удалось загрузить данные из базы данных.")
        return

    # Проверяем, есть ли столбец с датами
    if 'date' not in df.columns:
        print("Ошибка: В данных отсутствует столбец 'date'.")
        return

    # Преобразование даты в формат datetime
    df['date'] = pd.to_datetime(df['date'])

    # 1. Анализ продаж
    # Динамика продаж по дням, неделям, месяцам
    df['day'] = df['date'].dt.date
    df['week'] = df['date'].dt.isocalendar().week
    df['month'] = df['date'].dt.month

    # Выручка (totalPrice) и прибыль (finishedPrice)
    daily_sales = df.groupby('day')['totalPrice'].sum()

    # Средний чек
    if 'quantity' in df.columns:
        df['average_check'] = df['totalPrice'] / df['quantity']
    else:
        df['average_check'] = df['totalPrice']  # Если количество не указано

    # 2. Анализ заказов
    # Количество новых заказов
    if 'orderType' in df.columns:
        new_orders = df[df['orderType'] == 'Клиентский'].groupby('day').size()
    else:
        new_orders = df.groupby('day').size()  # Если тип заказа не указан

    # Статусы заказов
    if 'orderType' in df.columns:
        order_status = df['orderType'].value_counts()
    else:
        order_status = None

    # 3. Анализ остатков
    # Текущие остатки на складах
    if 'warehouseName' in df.columns and 'quantity' in df.columns:
        current_stock = df.groupby('warehouseName')['quantity'].sum()
    else:
        current_stock = None

    # Прогнозирование остатков (пример: на основе средних продаж)
    if current_stock is not None:
        average_daily_sales = daily_sales.mean()
        forecast_stock = current_stock - (average_daily_sales * 30)  # Прогноз на 30 дней
    else:
        forecast_stock = None

    # 4. Анализ возвратов
    # Процент возвратов
    if 'isCancel' in df.columns:
        total_orders = df.shape[0]
        returned_orders = df[df['isCancel'] == 1].shape[0]  # isCancel = 1 для возвратов
        return_percentage = (returned_orders / total_orders) * 100
    else:
        return_percentage = None

    # Причины возвратов (если данные доступны)
    if 'cancelReason' in df.columns:
        return_reasons = df['cancelReason'].value_counts()
    else:
        return_reasons = None

    # 5. Визуализация
    plt.figure(figsize=(15, 12))  # Увеличиваем размер фигуры для добавления нового графика

    # График динамики продаж по дням
    plt.subplot(3, 2, 1)
    daily_sales.plot(kind='line', title='Динамика продаж по дням')
    plt.xlabel('День')
    plt.ylabel('Выручка')

    # График количества новых заказов
    plt.subplot(3, 2, 2)
    new_orders.plot(kind='bar', title='Количество новых заказов по дням')
    plt.xlabel('День')
    plt.ylabel('Количество заказов')

    # График текущих остатков на складах (если данные доступны)
    if current_stock is not None:
        plt.subplot(3, 2, 3)
        current_stock.plot(kind='bar', title='Текущие остатки на складах')
        plt.xlabel('Склад')
        plt.ylabel('Количество')

    # График прогнозируемых остатков (если данные доступны)
    if forecast_stock is not None:
        plt.subplot(3, 2, 4)
        forecast_stock.plot(kind='bar', title='Прогнозируемые остатки через 30 дней')
        plt.xlabel('Склад')
        plt.ylabel('Количество')

    # Круговая диаграмма для возвратов (если данные доступны)
    if return_percentage is not None:
        plt.subplot(3, 2, 5)
        plt.pie([return_percentage, 100 - return_percentage], labels=['Возвраты', 'Остальные'], autopct='%1.1f%%')
        plt.title('Процент возвратов')

    # Сохраняем график в файл
    plt.tight_layout()
    plt.savefig('sales_analysis.png', dpi=300, bbox_inches='tight')  # Сохранение графика
    plt.show()

    # 6. Детализированные таблицы
    print("\nДетализированные данные:")
    print(df)  # Вывод всей таблицы

    # 7. Уведомления
    # Уведомление о критических остатках
    if current_stock is not None:
        critical_stock_threshold = 100  # Порог для критических остатков
        for warehouse, stock in current_stock.items():
            if stock < critical_stock_threshold:
                send_notification(f"Критические остатки на складе {warehouse}: {stock} единиц")

    # Уведомление о резком изменении продаж
    if len(daily_sales) > 1:
        sales_drop_threshold = 0.5  # Порог для падения продаж (50%)
        last_sales = daily_sales.iloc[-1]
        previous_sales = daily_sales.iloc[-2]
        if last_sales < previous_sales * (1 - sales_drop_threshold):
            send_notification(f"Резкое падение продаж: с {previous_sales} до {last_sales}")

    # Вывод дополнительной информации
    print(f"\nСредний чек: {df['average_check'].mean():.2f}")
    if return_percentage is not None:
        print(f"Процент возвратов: {return_percentage:.2f}%")
    if return_reasons is not None:
        print("Причины возвратов:")
        print(return_reasons)

    # Использование переменной order_status
    if order_status is not None:
        print("\nСтатусы заказов:")
        print(order_status)

    # Использование переменной forecast_stock
    if forecast_stock is not None:
        print("\nПрогнозируемые остатки на складах через 30 дней:")
        print(forecast_stock)
    else:
        print("\nПрогнозируемые остатки недоступны. Проверьте данные о текущих остатках и продажах.")


# Запуск функции
analyzing_sales()