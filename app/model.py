import aiogram

from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from samoware import Samoware
from storage.db import Storage


class MailBot(aiogram.Bot):
    def __init__(self, 
                 token: str,
                 mail: Samoware, 
                 db: Storage,
                 session = None, 
                 **kwargs):
        self._mail = mail
        self._db = db
        self.default = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
        super().__init__(token, session, self.default, **kwargs)
