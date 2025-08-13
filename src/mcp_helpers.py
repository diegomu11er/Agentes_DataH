
import ssl
import httpx
from typing import Any, List, Union
from xml.etree import ElementTree as ET
from smtplib import SMTP, SMTP_SSL
from pathlib import Path
from typing import List, Union
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

try:
    from email import encoders
except:
    from email import Encoders as encoders

import warnings
warnings.filterwarnings('ignore')

class ArxivHelper:

    @property
    def base_url(self):
        return 'https://export.arxiv.org/api/query'

    async def make_arxiv_request(self, url:str) -> str | None:
        async with httpx.AsyncClient() as client:
            try:            
                response = await client.get(url, headers={"User-Agent": 'arxiv-search-app/1.0'}, timeout=30)
                response.raise_for_status()
                return response.text
            except Exception as e:     
                print(e)       
                return None
            
    def parse_arxiv_response(self, xml_data:str) -> list[dict[str, Any]]:
        if not xml_data:
            return []
        
        root = ET.fromstring(xml_data)

        namespaces = {
            "atom": 'http://www.w3.org/2005/Atom',
            "arxiv": 'http://arxiv.org/schemas/atom'
        }

        entries = []
        for entry in root.findall('.//atom:entry', namespaces):
            e_title = entry.find('atom:title', namespaces)
            e_summary = entry.find('atom:summary', namespaces)
            e_link =  entry.find('atom:id', namespaces)
            e_published = entry.find('atom:published', namespaces)

            title = e_title.text.strip() if e_title is not None else ""
            summary = e_summary.text.strip() if e_summary is not None else ""

            authors = []
            for author in entry.findall('.//atom:author/atom:name', namespaces):
                authors.append(author.text.strip())

            link = e_link.text.strip() if e_link is not None else ""
            published = e_published.text.strip() if e_published is not None else ""

            entries.append(dict(
                title=title,
                summary=summary,
                authors=authors,
                link=link,
                published=published            
            ))

        return entries

    def format_paper(self, paper:dict) -> str:
        authors_str = " ".join(paper.get('authors', ['Unknown author']))
        return f"""
            title: {paper.get('title', '')}
            authors: {authors_str}
            published: {paper.get('published', '')[:10]}
            link: {paper.get('link', '')}
            summary: {paper.get('summary', '')}
        """
   

class MailRecipient(object):

    def __init__(self):
        self.__recipients: List = []

    def add(self, email: str, name: str = None):
        if not name:
            self.__recipients.append(email)
        else:
            self.__recipients.append(formataddr((name, email)))

    def clear(self):
        self.__recipients = []

    def get(self) -> str:
        return ', '.join(self.__recipients)

    def has_item(self) -> bool:
        if not self.__recipients:
            return False
        return len(self.__recipients) > 0
    

class MailMessage(object):

    def __init__(self, sender_email: str, sender_name: str = None):
        self.__message: MIMEMultipart = MIMEMultipart()
        self.__from: str = sender_email
        self.__from_name: str = sender_name
        self.__body: Union[str, None] = None
        self.__subject: Union[str, None] = None
        self.to: MailRecipient = MailRecipient()
        self.cc: MailRecipient = MailRecipient()
        self.bcc: MailRecipient = MailRecipient()

    def get_message(self) -> MIMEMultipart:
        self.__message['From'] = formataddr((self.__from_name, self.__from)) if self.__from_name else self.__from
        self.__message['Subject'] = self.__subject
        self.__message['To'] = self.to.get()
        if self.cc.has_item():
            self.__message['Cc'] = self.cc.get()
        if self.bcc.has_item():
            self.__message['Bcc'] = self.bcc.get()
        self.__message.attach(self.__body)
        self.__validate_mail_message()
        return self.__message

    def set_subject(self, subject: str):
        self.__subject = subject

    def set_text_body(self, text):
        self.__body = MIMEText(text, "plain")

    def set_html_body(self, html):
        self.__body = MIMEText(html, "html")

    def attach_file(self, filename: str, mime_type: str = "application/octet-stream"):
        with open(filename, 'rb') as attachment:
            mime_type_parts: List[str] = mime_type.split('/')
            part: MIMEBase = MIMEBase(mime_type_parts[0], mime_type_parts[1])
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {Path(filename).name}")
        self.__message.attach(part)

    def __validate_mail_message(self):
        if not self.__subject:
            raise ValueError("The email subject is required.")
        if not self.__body:
            raise ValueError("The email body is required.")
        if not self.__message['From']:
            raise ValueError('From is required.')
        if len(self.__message['From']) == 0:
            raise ValueError("The sender (from) is required.")
        if not self.to.has_item() and not self.cc.has_item() and not self.bcc.has_item():
            raise ValueError("Add at least a email to send this message.")


class SMTPServer(object):

    def __init__(self, host: str, port: int = 587,
                 username: str = None, password: str = None,
                 has_ssl: bool = False, has_tls: bool = True,
                 has_authentication: bool = True):
        
        self.__host: str = host
        self.__port: int = port
        self.__username: str = username
        self.__password: str = password
        self.__tls: bool = has_tls
        self.__ssl: bool = has_ssl
        self.__authentication: bool = has_authentication
        self.__context = ssl.create_default_context()

    def connect(self) -> Union[SMTP, SMTP_SSL]:
        try:
            if self.__tls:
                self.__server = SMTP(host=self.__host, port=self.__port)
                self.__server.ehlo()
                self.__server.starttls(context=self.__context)
                self.__server.ehlo()
            elif self.__ssl:
                self.__server = SMTP_SSL(host=self.__host, port=self.__port, context=self.__context)
            else:
                self.__server = SMTP(host=self.__host, port=self.__port)

            if self.__authentication:
                self.__server.login(user=self.__username, password=self.__password)

        except Exception as e:
            if self.__server:
                self.disconnect()
            raise e
        return self.__server

    def disconnect(self):
        self.__check_connection()
        self.__server.quit()

    def send(self, mail_message: MailMessage) -> bool:
        self.__check_connection()
        self.__server.send_message(msg=mail_message.get_message())
        return True

    def get_sender(self) -> str:
        return self.__username

    def __check_connection(self):
        if not self.__server:
            raise ConnectionError("The server is not connected. Connect first.")

