from typing import Optional, Union

import redis
import httpx
from lxml import etree

from samoware.exceptions.common_exceptions import AuthenticationError


class Samoware:
    def __init__(self,
                 host: str,
                 username: str,
                 password: str,
                 auth_url: str = 'ximsslogin/',
                 cached: bool = False,
                 storage: redis.Redis = None
                 ):

        if not host:
            raise ValueError
        if not username:
            raise ValueError
        if not password:
            raise ValueError
        # if cached and storage is None:
        #     raise ValueError('Add storage for caching request!')

        self._host: str = host
        self._user: str = username
        self._password: str = password
        self._session_key: Optional[str] = None
        self._auth_url: str = auth_url
        # self.cached = cached
        # self.storage = storage
        self._reqSeq: int = 0

    async def _make_session_key(self) -> None:
        """
        Сохраняет ключ аутентифицированного пользователя в стейт объекта.
        """
        # if await self.storage.get(self._user):
        #     self._session_key = (await self.storage.get(self._user)).decode()
        #     print('et')
        # else:
        token_body = await self._auth()
        root = etree.fromstring(token_body)
        self._session_key = f'Session/{root.xpath("//session/@urlID")[0]}'
        # print('no')
        return self._session_key  #TODO: должно сохранять в стейт объекта
        # await self.storage.setex(self._user, 1000, self._session_key)

    async def _auth(self) -> Union[Exception, str]:
        """
        Аутентифицирует пользователя в почте.

        :return: str - Вернет ответ серверва в формате строки.
        :raise AuthenticationError - не удалось аутентифицировать пользователя.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(url=self._host + self._auth_url,
                                        params={'username': self._user, 'password': self._password})
            if not response.status_code == 200:
                raise AuthenticationError(response.text)
            return response.text
        
    async def _open_mail_folder(self):
        async with httpx.AsyncClient() as client:
            self.session = await self._make_session_key()
            self._reqSeq += 1

            headers = {
                "accept": "*/*",
                "content-type": "application/xml;charset=UTF-8",
                "host": "student.bmstu.ru",
                "origin": "https://student.bmstu.ru",
                "referer": "https://student.bmstu.ru/",
            }

            base_url = f"{self._host}{self.session}/sync?reqSeq={self._reqSeq}&random={self._reqSeq}"
            
            payload = \
            """
            <XIMSS>
                <folderOpen mailbox="INBOX" sortField="INTERNALDATE" sortOrder="desc" folder="INBOX-MM-1" id="16">
                    <field>FLAGS</field>
                    <field>E-From</field>
                    <field>Subject</field>
                    <field>Pty</field>
                    <field>Content-Type</field>
                    <field>INTERNALDATE</field>
                    <field>SIZE</field>
                    <field>E-To</field>
                    <field>E-Cc</field>
                    <field>E-Reply-To</field>
                    <field>X-Color</field>
                    <field>Disposition-Notification-To</field>
                    <field>X-Request-DSN</field>
                    <field>References</field>
                    <field>Message-ID</field>
                </folderOpen>
                <setSessionOption name="reportMailboxChanges" value="yes" id="17"/>
            </XIMSS>
            """
            
            response = await client.post(base_url, headers=headers, data=payload)
            print(f"Открытие папки: {response.status_code}")
            print(response.text)

            if response.status_code != 200:
                print("Ошибка при открытии папки.")
                return None
            
            
    async def parse_mail(self):
        async with httpx.AsyncClient() as client:
            # Убедимся, что сессия создана
            # if self.session is None:
            self.session = await self._make_session_key()
            if self.session is None:
                print("Ошибка: Не удалось создать сессию.")
                return "err"
            
            await self._open_mail_folder()

            # Увеличиваем reqSeq для каждого запроса
            self._reqSeq += 1

            headers = {
                "accept": "*/*",
                "content-type": "application/xml;charset=UTF-8",
                "host": "student.bmstu.ru",
                "origin": "https://student.bmstu.ru",
                "referer": "https://student.bmstu.ru/",
            }

            base_url = f"{self._host}{self.session}/sync?reqSeq={self._reqSeq}&random={self._reqSeq}"

            # Шаг 1: Открываем папку с необходимыми полями
            open_folder_payload = \
            """
            <XIMSS>
                <folderOpen mailbox="INBOX" sortField="INTERNALDATE" sortOrder="desc" folder="INBOX-MM-1" id="16">
                    <field>FLAGS</field>
                    <field>E-From</field>
                    <field>Subject</field>
                    <field>Pty</field>
                    <field>Content-Type</field>
                    <field>INTERNALDATE</field>
                    <field>SIZE</field>
                    <field>E-To</field>
                    <field>E-Cc</field>
                    <field>E-Reply-To</field>
                    <field>X-Color</field>
                    <field>Disposition-Notification-To</field>
                    <field>X-Request-DSN</field>
                    <field>References</field>
                    <field>Message-ID</field>
                </folderOpen>
                <setSessionOption name="reportMailboxChanges" value="yes" id="17"/>
            </XIMSS>
            """
            
            open_folder_response = await client.post(base_url, headers=headers, data=open_folder_payload)
            print(f"Открытие папки: {open_folder_response.status_code}")
            print(open_folder_response.text)

            if open_folder_response.status_code != 200:
                print("Ошибка при открытии папки.")
                return None

            # Шаг 2: Выполняем запрос на просмотр писем
            self._reqSeq += 1
            idx_from = 0
            idx_to = 3
            browse_folder_payload = \
            f"""
            <XIMSS>
                <folderBrowse folder="INBOX-MM-1" id="19">
                    <index from="{idx_from}" till="{idx_to}"/>
                </folderBrowse>
            </XIMSS>
            """
            response = await client.post(
                f"{self._host}{self.session}/sync?reqSeq={self._reqSeq}&random={self._reqSeq}",
                headers=headers,
                data=browse_folder_payload
            )
            print(f"HTTP Status: {response.status_code}")
            print(f"Response Text: {response.text}")

            # Обработка ответа
            if response.status_code == 200:
                print("Письма получены успешно!")
                return response.text
            else:
                print(f"Ошибка: {response.status_code}")
                return None
