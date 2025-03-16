import os

def is_writable(directory):
    """Проверяет, можно ли записывать файлы в указанную папку."""
    test_file = os.path.join(directory, "test_write_permission.tmp")
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        return True
    except PermissionError: return False

def get_save_path():
    path_file = 'save_path.txt'

    if os.path.exists(path_file):
        with open(path_file, 'r') as f:
            saved_path = f.read().strip()
            if saved_path and is_writable(saved_path):
                change_path = input("Хотите изменить путь? (да/нет): ").strip().lower()
                if change_path == 'нет':
                    return saved_path
            else:
                print(f"⚠️ Внимание: В папку '{saved_path}' нельзя записывать файлы!")

    while True:
        new_path = input("Введите новый путь для сохранения: ").strip()
        if not os.path.exists(new_path):
            try:
                os.makedirs(new_path)
            except PermissionError:
                print(f"⚠️ Ошибка: Нет прав для создания папки '{new_path}'. Попробуйте другой путь.")
                continue

        if is_writable(new_path):
            with open(path_file, 'w') as f:
                f.write(new_path)
            return new_path
        else:
            print(f"⚠️ Внимание: В папку '{new_path}' нельзя записывать файлы! Попробуйте другой путь.")
