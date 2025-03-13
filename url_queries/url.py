# URL для запроса данных (основные).
BASIC_URL = {
    'Orders': {
        'url': 'https://statistics-api.wildberries.ru/api/v1/supplier/orders',
        'params_template': {'dateFrom': None, 'flag': 0} # Заказы
    },
    'Sales': {
        'url': 'https://statistics-api.wildberries.ru/api/v1/supplier/sales',
        'params_template': {'dateFrom': None, 'flag': 0} # Продажи
    },
    'Remains': {
        'url': 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks',
        'params_template': {'dateFrom': None} # Остатки
    },
    'Refunds': {
        'url': 'https://statistics-api.wildberries.ru/api/v1/supplier/returns',
        'params_template': {'dateFrom': None} # Возвраты
    },
    'Sales_Report': {
        'url': 'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod',
        'params_template': {'dateFrom': None, 'dateTo': None} # Отчет о продажах
    },
    'Balance': {
        'url': 'https://statistics-api.wildberries.ru/api/v1/supplier/balance',
        'params_template': {'dateFrom': None, 'dateTo': None} # Баланс денег
    }
}

# URL для запроса данных (доп).
ADD_URL = {
    'Product_Information': {
        'url': 'https://suppliers-api.wildberries.ru/api/v2/stocks',
        'params_template': {'dateFrom': None} # Информация о продукте
    },
    'Product_rating': {
        'url': 'https://suppliers-api.wildberries.ru/api/v1/supplier/products/rating',
        'params_template': {'dateFrom': None} # Рейтинг продукта
    },
    'Delivery_Information': {
        'url': 'https://suppliers-api.wildberries.ru/api/v1/supplier/incomes',
        'params_template': {'dateFrom': None} # Информация о поставках
    },
    'Information_about_payments': {
        'url': 'https://suppliers-api.wildberries.ru/api/v1/supplier/payments',
        'params_template': {'dateFrom': None} # Информация о выплатах
    }
}
