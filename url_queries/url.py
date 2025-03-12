# URL для запроса данных (основные).
basic_url = {
    'Orders': {
        'url': 'https://statistics-api.wildberries.ru/api/v1/supplier/orders',
        'params_template': {'date_from': None, 'flag': 0} # Заказы
    },
    'Sales': {
        'url': 'https://statistics-api.wildberries.ru/api/v1/supplier/sales',
        'params_template': {'date_from': None, 'flag': 0} # Продажи
    },
    'Remains': {
        'url': 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks',
        'params_template': {'date_from': None} # Остатки
    },
    'Refunds': {
        'url': 'https://statistics-api.wildberries.ru/api/v1/supplier/returns',
        'params_template': {'date_from': None} # Возвраты
    },
    'Sales_Report': {
        'url': 'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod',
        'params_template': {'date_from': None, 'date_to': None} # Отчет о продажах
    }
}

# URL для запроса данных (доп).
add_url = {
    'Product_Information': {
        'url': 'https://suppliers-api.wildberries.ru/api/v2/stocks',
        'params_template': {'date_from': None} # Информация о продукте
    },
    'Product_rating': {
        'url': 'https://suppliers-api.wildberries.ru/api/v1/supplier/products/rating',
        'params_template': {'date_from': None} # Рейтинг продукта
    },
    'Delivery_Information': {
        'url': 'https://suppliers-api.wildberries.ru/api/v1/supplier/incomes',
        'params_template': {'date_from': None} # Информация о поставках
    },
    'Information_about_payments': {
        'url': 'https://suppliers-api.wildberries.ru/api/v1/supplier/payments',
        'params_template': {'date_from': None} # Информация о выплатах
    }
}
