# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'test@nxin.com'
password = 'xxxxxxxx'
receivers = ['liuyang@nxin.com']

message = MIMEText('<h1>Hello World</h1>', 'html', 'utf-8')
message['Subject'] = Header('Python 测试邮件', 'utf-8')

try:
    smtpObj = smtplib.SMTP("smtp.qiye.163.com")
    smtpObj.login(sender, password)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print(e)
