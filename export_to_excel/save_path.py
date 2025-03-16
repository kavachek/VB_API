import os

def get_save_path():
    path_file = 'save_path.txt'

    if os.path.exists(path_file):
        with open(path_file, 'r') as f:
            saved_path = f.read().strip()
            if saved_path:
                change_path = input("Хотите изменить путь? (да/нет): ").strip().lower()
                if change_path == 'да':
                    new_path = input("Введите новый путь для сохранения: ").strip()
                    if not os.path.exists(new_path):
                        os.makedirs(new_path)
                    with open(path_file, 'w') as file:
                        file.write(new_path)
                    return new_path
                return saved_path
    else:
        new_path = input("Введите путь для сохранения: ").strip()
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        with open(path_file, 'w') as f:
            f.write(new_path)
        return new_path
