# coding=utf-8
"""
邮件上报模块
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from LogHelper import Log


class MailReporter:

    TAG = "MailReporter"

    def __init__(self, sender, passwd, smtpHost, smtpPort, sendType):
        self.mailHost = smtpHost
        self.mailPort = smtpPort
        self.sender = sender
        self.passwd = passwd
        self.sendType = sendType

    def send(self, receivers, title, content, attachment=None):
        """
        send an Email to multiple receivers, attachment is optional
        :param receivers: list of receivers
        :param title:
        :param content:
        :param attachment: the file name for attachment, could be None
        :return:
        """
        if attachment:
            self._sendWithAttachment(receivers, title, content, attachment)
        else:
            self._sendText(receivers, title, content)

    def _sendText(self, receivers, title, content):
        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = title
        # 发送方信息
        message['From'] = self.sender
        # 接受方信息
        message['To'] = receivers[0]
        try:
            smtpObj = smtplib.SMTP_SSL() if self.sendType == "ssl" else smtplib.SMTP()
            # 连接到服务器
            smtpObj.connect(self.mailHost, self.mailPort)
            smtpObj.ehlo()
            if self.sendType == "tls":
                smtpObj.starttls()
            # 登录到服务器
            smtpObj.login(self.sender, self.passwd)
            # 发送
            smtpObj.sendmail(self.sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            Log.i(MailReporter.TAG, 'Mail successfully sent to ' + receivers[0])
        except smtplib.SMTPException as e:
            Log.e(MailReporter.TAG, 'send() error', e)

    def _sendWithAttachment(self, receivers, title, content, attachment=None):
        # 设置eamil信息
        # 添加一个MIMEmultipart类，处理正文及附件
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = receivers[0]
        message['Subject'] = title
        part = MIMEApplication(open(attachment, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=attachment)
        # 将内容附加到邮件主体中
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        message.attach(part)

        # 登录并发送
        try:
            smtpObj = smtplib.SMTP_SSL() if self.sendType == "ssl" else smtplib.SMTP()
            smtpObj.connect(self.mailHost, self.mailPort)
            smtpObj.ehlo()
            if self.sendType == "tls":
                smtpObj.starttls()
            smtpObj.login(self.sender, self.passwd)
            smtpObj.sendmail(self.sender, receivers, message.as_string())
            Log.i(MailReporter.TAG, 'Mail successfully sent to ' + receivers[0])
            smtpObj.quit()
        except smtplib.SMTPException as e:
            Log.e(MailReporter.TAG, 'send() error', e)
