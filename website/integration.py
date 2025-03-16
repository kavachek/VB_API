from flask import Flask, jsonify, request
from flask_cors import CORS  # Импортируем CORS

app = Flask(__name__)
CORS(app)  # Включаем CORS для всех маршрутов

@app.route("/online_stats", methods=["GET"])
def online_stats():
    try:
        data = {
            "today_orders": 150,
            "monthly_orders": 3200,
            "monthly_revenue": 45000,
            "order_sources": [
                {"source": "Москва", "count": 1200},
                {"source": "Питер", "count": 800},
                {"source": "Новосибирск", "count": 400}
            ]
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
