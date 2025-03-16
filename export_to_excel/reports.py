from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from classification_of_data.analyzing_everything import analyzing_sales, analyzing_stocks
from export_excel import export_sales_report, export_stocks_report

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

def is_writable(directory):
    test_file = os.path.join(directory, "test_write_permission.tmp")
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        return True
    except PermissionError: return False


def get_saved_path():
    """Возвращает путь, сохраненный в файле save_path.txt, или None, если файл пуст или не существует."""
    path_file = 'save_path.txt'
    if os.path.exists(path_file):
        with open(path_file, 'r') as f:
            path = f.read().strip()
            if path: return path
    return None


app.route('/save_path', methods=['POST'])
def save_path_to_file():
    """Сохраняет путь в файл save_path.txt."""
    data = request.json
    path = data.get('path')

    if not path: return jsonify({"error": "Не указан путь для сохранения."}), 400

    try:
        with open('save_path.txt', 'w') as f:
            f.write(path)
        return jsonify({"message": "Путь сохранен успешно."}), 200
    except Exception as e: return jsonify({"error": f"Ошибка при сохранении пути: {str(e)}"}), 500


@app.route('/generate_report', methods=['POST', 'OPTIONS'])
def generate_report():
    """Генерирует отчет на основе переданных данных."""
    if request.method == 'OPTIONS': return jsonify(), 200

    data = request.json

    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    report_type = data.get('report_type')

    if not start_date_str or not end_date_str or not report_type: return jsonify({"error": "Не все данные были"
                                                                                           " переданы."}), 400
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError: return jsonify({"error": "Неверный формат даты."}), 400

    # Получаем сохраненный путь из файла
    save_path_dir = get_saved_path()

    if not save_path_dir: return jsonify({"error": "Путь для сохранения не указан и не сохранен"
                                                   " в файле save_path.txt."}), 400

    if not os.path.exists(save_path_dir):
        try:
            os.makedirs(save_path_dir, exist_ok=True)
        except PermissionError: return jsonify({"error": f"Нет прав на создание папки: {save_path_dir}"}), 500

    results = {}

    try:
        if report_type == "sales":
            sales_results = analyzing_sales(start_date, end_date)
            export_sales_report(sales_results, save_path_dir, start_date, end_date)
            results["sales"] = "Отчет по заказам создан."

        elif report_type == "stocks":
            stocks_results = analyzing_stocks()
            export_stocks_report(stocks_results, save_path_dir, start_date, end_date)
            results["stocks"] = "Отчет по остаткам создан."

        elif report_type == "both":
            sales_results = analyzing_sales(start_date, end_date)
            stocks_results = analyzing_stocks()
            export_sales_report(sales_results, save_path_dir, start_date, end_date)
            export_stocks_report(stocks_results, save_path_dir, start_date, end_date)
            results["both"] = "Оба отчета созданы."

        else: return jsonify({"error": "Неверный тип отчета."}), 400

    except Exception as e:  return jsonify({"error": f"Ошибка при генерации отчета: {str(e)}"}), 500

    return jsonify({"message": "Отчет создан.", "results": results}), 200


if __name__ == "__main__":
    app.run(debug=True)
