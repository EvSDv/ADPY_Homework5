import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self, mail_name, password,
                 smtp='smtp.gmail.com', imap='imap.gmail.com'):
        self.mail_name = mail_name
        self.password = password
        self.smtp_server = smtp
        self.imap_server = imap

    def send_mail(self, recipients, subject, message_text):
        message = MIMEMultipart()
        message['From'] = self.mail_name
        message['To'] = ', '.join(recipients)
        message['Subject'] = subject
        message.attach(MIMEText(message_text))

        client_smtp = smtplib.SMTP(self.smtp_server, 587)
        client_smtp.ehlo()
        client_smtp.starttls()
        client_smtp.ehlo()
        client_smtp.login(self.mail_name, self.password)
        client_smtp.sendmail(self.mail_name, recipients, message.as_string())
        client_smtp.quit()

    def receive_mail(self, header=None):
        client_imap = imaplib.IMAP4_SSL(self.imap_server)
        client_imap.login(self.mail_name, self.password)
        client_imap.list()
        client_imap.select('inbox')
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = client_imap.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = client_imap.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        client_imap.logout()
        return email_message


if __name__ == '__main__':
    mailbox = Mail('vyacheslav.eyhe@gmail.com', 'XXXXXXXXXXX')
    mailbox.send_mail(['eyhev@mail.ru', 'eykhe.vyacheslav@sogaz-med.ru'],
                      'Test', 'Text message')
    mailbox.receive_mail()
