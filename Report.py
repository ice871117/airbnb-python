"""
邮件上报模块
"""
import smtplib
from email.mime.text import MIMEText

class MailReporter:

    @staticmethod
    def getSMTPAddress(sender):
        index = sender.find("@")
        if index > 0:
            return "smtp.{0}".format(sender[index + 1:])

    def __init__(self, sender, passwd):
        self.mailHost = MailReporter.getSMTPAddress(sender)
        self.sender = sender
        self.passwd = passwd


    def send(self, receivers, title, content):
        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = title
        # 发送方信息
        message['From'] = self.sender
        # 接受方信息
        message['To'] = receivers
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            smtpObj.connect(self.mailHost, 25)
            # 登录到服务器
            smtpObj.login(self.sender, self.passwd)
            # 发送
            smtpObj.sendmail(self.sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            print('success')
        except smtplib.SMTPException as e:
            print('error', e)  # 打印错误
