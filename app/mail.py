import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from samoware import Samoware


async def main():
    sw = Samoware(
        host='https://student.bmstu.ru/',
        username='aad24u790',
        password='ck9d6bdw',
    )
    # res = await sw.auth()
    # s = await sw.make_session_key()
    # print(res)
    # print(s)
    # mail = await sw.parse_mail()
    mail = await sw._open_mail_folder()
    print(mail)


async def get_mail(host: str, user: str, password: str) -> Samoware:
    pass


if __name__ == "__main__":
    asyncio.run(main())
