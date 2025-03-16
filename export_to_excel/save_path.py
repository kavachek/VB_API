from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def is_writable(directory):
    test_file = os.path.join(directory, "test_write_permission.tmp")
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        return True
    except PermissionError: return False

@app.route('/save_path', methods=['POST'])
def save_path():
    data = request.json
    new_path = data.get('path')

    if not new_path: return jsonify({"error": "Путь не указан."}), 400

    if not os.path.exists(new_path):
        try:
            os.makedirs(new_path)
        except PermissionError: return jsonify({"error": f"⚠️ Ошибка: Нет прав для создания папки '{new_path}'."}), 400

    if not is_writable(new_path): return jsonify({"error": f"⚠️ Внимание: В папку '{new_path}'"
                                                           f" нельзя записывать файлы!"}), 400

    path_file = 'save_path.txt'
    with open(path_file, 'w') as f:
        f.write(new_path)

    return jsonify({"message": f"Путь '{new_path}' успешно сохранен."}), 200

if __name__ == '__main__':
    app.run(debug=True)
