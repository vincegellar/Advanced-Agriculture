import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import configparser
from os import path

config = configparser.RawConfigParser()
config.read(path.join(path.dirname(__file__), '../EnvironmentHandler.cfg'))
from_addr = config.get('Email', 'address')
smtp_server = config.get('Email', 'server')
server_port = config.getint('Email', 'port')


class Mailer:

    def __init__(self):
        self.from_address = from_addr

    def send_water_level_low(self, *addresses):
        message = MIMEMultipart()
        message['From'] = self.from_address
        locale = self.load_locale('en-US')
        message['Subject'] = locale['low-water-level']['subject']
        body = locale['low-water-level']['body']
        message.attach(MIMEText(body, 'plain'))
        self.send_mail(message, addresses)

    def load_locale(self, code):
        with open(path.join(path.dirname(__file__), '../Localisation/emails.json')) as localisation_file:
            locales = json.load(localisation_file)
        return locales[code]

    def send_mail(self, message: MIMEMultipart, *addresses):
        server = smtplib.SMTP(smtp_server, server_port)
        server.connect(smtp_server, server_port)
        server.starttls()
        server.ehlo()
        server.login(self.from_address, "YOUR PASSWORD")
        server.starttls()
        for addr in addresses:
            message['To'] = addr[0]
            text = message.as_string()
            server.sendmail(self.from_address, addr, text)
        server.quit()
