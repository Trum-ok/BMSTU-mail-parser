import redis
import time


class RedisStorage:
    def __init__(self, host: str, port: int = 6379, db: int = 0, expire_time: int = 120):
        """
        Инициализация соединения с Redis.
        
        :param host: Хост Redis-сервера.
        :param port: Порт Redis-сервера.
        :param db: Номер базы данных Redis.
        :param expire_time: Время жизни записи в секундах (по умолчанию 120 секунд).
        """
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        self.expire_time = expire_time

    def add_user(self, username: str, session: str) -> bool:
        """
        Добавляет сессию пользователя в Redis с ограниченным временем жизни.
        
        :param username: Имя пользователя.
        :param session: Сессионный идентификатор.
        :return: True, если операция успешна.
        """
        return self.client.setex(f"user:{username}", self.expire_time, session)

    def get_user_session(self, username: str) -> str:
        """
        Возвращает сессию пользователя.
        
        :param username: Имя пользователя.
        :return: Сессионный идентификатор или None, если запись отсутствует.
        """
        return self.client.get(f"user:{username}")

    def delete_user(self, username: str) -> bool:
        """
        Удаляет пользователя из Redis.
        
        :param username: Имя пользователя.
        :return: True, если операция успешна.
        """
        return self.client.delete(f"user:{username}") > 0

    def update_user_session(self, username: str, new_session: str) -> bool:
        """
        Обновляет сессию пользователя и сбрасывает таймер времени жизни.
        
        :param username: Имя пользователя.
        :param new_session: Новый сессионный идентификатор.
        :return: True, если операция успешна.
        """
        return self.client.setex(f"user:{username}", self.expire_time, new_session)

    def get_all_users(self) -> dict:
        """
        Возвращает всех пользователей и их сессии.
        
        :return: Словарь пользователей и их сессий.
        """
        keys = self.client.keys("user:*")
        users = {key.split(":")[1]: self.client.get(key) for key in keys}
        return users


if __name__ == "__main__":
    storage = RedisStorage(expire_time=120)

    # Добавление пользователей
    storage.add_user("user1", "session1")
    storage.add_user("user2", "session2")

    # Получение сессии пользователя
    print(storage.get_user_session("user1"))  # Вывод: session1

    # Обновление сессии пользователя
    storage.update_user_session("user1", "new_session1")

    # Проверка обновленной сессии
    print(storage.get_user_session("user1"))  # Вывод: new_session1

    # Получение всех пользователей
    print(storage.get_all_users())  # Вывод: {'user1': 'new_session1', 'user2': 'session2'}

    # Удаление пользователя
    storage.delete_user("user2")
    print(storage.get_all_users())  # Вывод: {'user1': 'new_session1'}
