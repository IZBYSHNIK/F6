import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version
import random

class Postman:
    def __init__(self):
        self.user = 'kgkf6@mail.ru'
        self.password = 'jCXjwMAT4XrEBbpTw0Rt'
        self.server = 'smtp.mail.ru'
        self.recipients = ['il.rahmatullin50@gmail.com']
        self.cod = self.generate_cod()
        self.html = MIMEText(f"""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv = "content-type" content = "text/html; charset = utf-8" >
    <style type="text/css">
        #cod {{
        color: red;
        font: 16px sans-serif bold;
        font-size: 30px;
        }}
        .content p {{
            font: 14px sans-serif;
        }}
    </style>
</head>
<body>
<div class="content">
    <h2>Здравствуйте!</h2>
    <p>Вы отправили запрос на привязку почты к аккаунту F6.</p>
    <p>Для того чтобы привязку почтe, используйте код <span id="cod">{self.cod}</span> и следуйте инструкциям в приложении.</p>
    <p>Пожалуйста, проигнорируйте данное письмо, если оно попало к Вам по ошибке.</p>
    <p>С уважением, Служба поддержки пользователей проекта F6.</p>
</div>
</body>
</html>""", 'html')
        self.sender = 'kgkf6@mail.ru'
        self.subject = 'Код для привязки к аккаунту f6'

        self.init_letter()

    def init_letter(self):
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.sender
        self.msg['To'] = ', '.join(self.recipients)
        self.msg['Reply-To'] = self.sender
        self.msg['Return-Path'] = self.sender
        self.msg['X-Mailer'] = 'Python/' + (python_version())
        self.msg.attach(self.html)

    def send(self):
        mail = smtplib.SMTP_SSL(self.server, 465)
        mail.login(self.user, self.password)
        mail.sendmail(self.sender, self.recipients, self.msg.as_string())
        mail.quit()

    def generate_cod(self, len_cod=8):
        return ''.join([[chr(random.randint(65, 90)), chr(random.randint(48, 57))][random.randint(0, 1)] for _ in range(len_cod)])

    def check_cod(self, cod):
        if self.cod == cod:
            self.cod = self.generate_cod()
            return cod
        raise ValueError('Введен неверный код подтверждения')



postman = Postman()
postman.send()








