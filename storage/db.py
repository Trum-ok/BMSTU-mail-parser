import os
import json

from typing import Optional


class Storage:
    def __init__(self, file_path: str = "storage.json"):
        self.file_path = file_path
        # Создаем файл, если его нет
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({"users": {}}, f)

    def _load_data(self) -> dict:
        """Загружает данные из JSON-файла."""
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _save_data(self, data: dict) -> None:
        """Сохраняет данные в JSON-файл."""
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def add_user(self, username: str, hashed_password: str) -> bool:
        """Добавляет пользователя."""
        data = self._load_data()
        if username in data["users"]:
            return False  # Пользователь уже существует
        data["users"][username] = hashed_password
        self._save_data(data)
        return True

    def edit_user(self, username: str, new_hashed_password: str) -> bool:
        """Редактирует данные пользователя."""
        data = self._load_data()
        if username not in data["users"]:
            return False  # Пользователь не найден
        data["users"][username] = new_hashed_password
        self._save_data(data)
        return True

    def delete_user(self, username: str) -> bool:
        """Удаляет пользователя."""
        data = self._load_data()
        if username not in data["users"]:
            return False  # Пользователь не найден
        del data["users"][username]
        self._save_data(data)
        return True

    def find_user(self, username: str) -> Optional[str]:
        """Ищет пользователя."""
        data = self._load_data()
        return data["users"].get(username)  # Возвращает пароль или None

    def get_all_users(self) -> dict:
        """Возвращает всех пользователей."""
        data = self._load_data()
        return data["users"]


if __name__ == "__main__":
    storage = Storage()

    # Добавление пользователей
    storage.add_user("user1", "hashed_pass1")
    storage.add_user("user2", "hashed_pass2")

    # Редактирование пользователя
    storage.edit_user("user1", "new_hashed_pass1")

    # Поиск пользователя
    print(storage.find_user("user1"))  # Вывод: new_hashed_pass1

    # Удаление пользователя
    storage.delete_user("user2")

    # Получение всех пользователей
    print(storage.get_all_users())  # Вывод: {'user1': 'new_hashed_pass1'}
