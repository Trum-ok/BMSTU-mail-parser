from __future__ import annotations

import xml.etree.ElementTree as ET


class Folder:
    def __init__(self,
                 name: str = None,
                 mode: str = None,
                 msg_cnt: int = None,
                 unseen_cnt: int = None
                 ):
        self.name = name
        self.mode = mode
        self.msg_cnt = msg_cnt
        self.unseen_cnt = unseen_cnt
    
    def __repr__(self):
        return f"Folder(name={self.name}, mode={self.mode}, msg_cnt={self.msg_cnt}, unseen_cnt={self.unseen_cnt})"
    
    def parse(self, xml: str) -> list[Folder]:
        root = ET.fromstring(xml)
        
        error = root.find('response')
        if error is not None and 'errorText' in error.attrib:
            print(f"Ошибка: {error.attrib['errorText']}")
            return []
        
        folders = []
        for folder in root.findall('.//folderReport'):
            name = folder.find('folder').text if folder.find('Name') is not None else None
            mode = folder.find('mode').text if folder.find('mode') is not None else None
            msg_cnt = folder.find('messages').text if folder.find('messages') is not None else None
            unseen_cnt = folder.find('unseen').text if folder.find('unseen') is not None else None

            folder = Folder(name, mode, msg_cnt, unseen_cnt)
            folders.append(folder)
        return folders
    

class Mail:
    def __init__(self, 
                 flags: list = [],
                 e_from: str = None,
                 subject: str = None,
                 pty: str = None,
                 content_type: str = None,
                 date: str = None,
                 size: str = None,
                 e_to: list = [],
                 x_color: str = None,
                 msg_id: str = None,
                 ):
        self.flags = flags
        self.e_from = e_from
        self.subject = subject
        self.pty = pty
        self.content_type = content_type
        self.date = date
        self.size = size
        self.e_to = e_to
        self.x_color = x_color
        self.msg_id = msg_id
    
    def __repr__(self):
        return f"Mail(from={self.e_from}, subject={self.subject}, date={self.date}, content-type={self.content_type})"

    def parse(self, xml: str) -> list[Mail]:
        """
        """
        root = ET.fromstring(xml)
        
        error = root.find('response')
        if error is not None and 'errorText' in error.attrib:
            print(f"Ошибка: {error.attrib['errorText']}")
            return []
        
        mails: list[Mail] = []
        for mail_item in root.findall('.//folderReport'):
            flags = mail_item.find('FLAGS').text if mail_item.find('FLAGS') is not None else []
            e_from = mail_item.find('E-From').text if mail_item.find('E-From') is not None else None
            pty = mail_item.find('Pty').text if mail_item.find('Pty') is not None else None
            subject = mail_item.find('Subject').text if mail_item.find('Subject') is not None else None
            content_type = mail_item.find('Content-Type').text if mail_item.find('Content-Type') is not None else None
            date = mail_item.find('INTERNALDATE').text if mail_item.find('INTERNALDATE') is not None else None
            size = int(mail_item.find('SIZE').text) if mail_item.find('SIZE') is not None else 0
            e_to = mail_item.find('E-To').text if mail_item.find('E-To') is not None else []
            msg_id = mail_item.find('Message-ID').text if mail_item.find('Message-ID') is not None else None
            x_color = mail_item.find('X-Color').text if mail_item.find('X-Color') is not None else None
            
            mail = Mail(
                flags = flags,
                e_from = e_from,
                subject = subject,
                pty = pty,
                content_type = content_type,
                date = date,
                size = size,
                e_to = e_to,
                x_color = x_color,
                msg_id = msg_id
            )
            mails.append(mail)

        return mails


if __name__ == "__main__":
    xml = """<XIMSS><folderReport id="19" folder="INBOX-MM-1" index="0" UID="78"><FLAGS>Seen</FLAGS><E-From realName="Кобцев Иван Федорович">kobcev@bmstu.ru</E-From><Subject>Досдача</Subject><Content-Type>multipart/alternative;boundary=&quot;_===57662285====bmstu.ru===_&quot;</Content-Type><INTERNALDATE localTime="20250107T182428">20250107T152428Z</INTERNALDATE><SIZE>1872</SIZE><E-To realName="ИУ7-16Б">group-iu7-16b@bmstu.ru</E-To><Message-ID>&lt;ximss-57662339@bmstu.ru&gt;</Message-ID></folderReport><folderReport id="19" folder="INBOX-MM-1" index="1" UID="77"><FLAGS>Seen</FLAGS><E-From realName="Яковлева Ольга Викторовна">oyakovleva@bmstu.ru</E-From><Subject>Результаты РК №3</Subject><Content-Type>multipart/mixed;boundary=&quot;_===57650716====bmstu.ru===_&quot;</Content-Type><INTERNALDATE localTime="20250104T162528">20250104T132528Z</INTERNALDATE><SIZE>349945</SIZE><E-To realName="ИУ7-16Б">group-iu7-16b@bmstu.ru</E-To><Message-ID>&lt;ximss-57650818@bmstu.ru&gt;</Message-ID></folderReport><folderReport id="19" folder="INBOX-MM-1" index="2" UID="76"><FLAGS>Seen</FLAGS><E-From realName="Головина Анастасия Михайловна">amgolovina@bmstu.ru</E-From><Subject>Расписание присутствия преподавателей кафедры ФН-12 в январе</Subject><Pty>High</Pty><Content-Type>multipart/mixed;boundary=&quot;_===57620267====bmstu.ru===_&quot;</Content-Type><INTERNALDATE localTime="20241228T140631">20241228T110631Z</INTERNALDATE><SIZE>732269</SIZE><E-To realName="group-iu4-11b@bmstu.ru">group-iu4-11b@bmstu.ru</E-To><E-To realName="group-iu4i-11b@bmstu.ru">group-iu4i-11b@bmstu.ru</E-To><E-To realName="group-iu4-12b@bmstu.ru">group-iu4-12b@bmstu.ru</E-To><E-To realName="group-iu4-13b@bmstu.ru">group-iu4-13b@bmstu.ru</E-To><E-To realName="ИУ7-11Б">group-iu7-11b@bmstu.ru</E-To><E-To realName="ИУ7-12Б">group-iu7-12b@bmstu.ru</E-To><E-To realName="ИУ7-13Б">group-iu7-13b@bmstu.ru</E-To><E-To realName="ИУ7-14Б">group-iu7-14b@bmstu.ru</E-To><E-To realName="ИУ7-15Б">group-iu7-15b@bmstu.ru</E-To><E-To realName="ИУ7-16Б">group-iu7-16b@bmstu.ru</E-To><E-To realName="ИУ7И-11Б">group-iu7i-11b@bmstu.ru</E-To><E-To realName="ИУ7И-12Б">group-iu7i-12b@bmstu.ru</E-To><E-To realName="ИУ7И-13Б">group-iu7i-13b@bmstu.ru</E-To><E-To realName="ИУ7И-14Б">group-iu7i-14b@bmstu.ru</E-To><E-To realName="ИУ7И-15Б">group-iu7i-15b@bmstu.ru</E-To><E-To realName="ИУ7И-17Б">group-iu7i-17b@bmstu.ru</E-To><Message-ID>&lt;ximss-57620277@bmstu.ru&gt;</Message-ID></folderReport><folderReport id="19" folder="INBOX-MM-1" index="3" UID="75"><FLAGS>Seen</FLAGS><E-From realName="GitHub">noreply@github.com</E-From><Subject>[GitHub] A third-party OAuth application has been added to your account</Subject><Content-Type>text/plain; charset=UTF-8</Content-Type><INTERNALDATE localTime="20241228T030856">20241228T000856Z</INTERNALDATE><SIZE>3004</SIZE><E-To realName="Trum">artamarkan@gmail.com</E-To><X-Color>navy</X-Color><Message-ID>&lt;676f419284174_a421fc2576c7@lowworker-6dd898464b-njrgs.mail&gt;</Message-ID></folderReport><response id="19"/></XIMSS>"""
    p = Mail()
    mails = p.parse(xml)
    print(mails[1])
