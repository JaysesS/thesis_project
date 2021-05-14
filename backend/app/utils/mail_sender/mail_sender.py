import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.mail_sender.mail_config import MAIL_LOGIN, MAIL_PASSWORD

def send_email(subject, body_text, to_addr, login = MAIL_LOGIN, password = MAIL_PASSWORD,  html=None):
    """
        Метод отправки эл. письма
        to_addr: str - список email аддресов, если несколько, указать через запятую
    """
    host = 'smtp.gmail.com'
    from_addr = login
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = login
    msg["To"] = to_addr

    part1 = MIMEText(body_text, "plain", "utf8")
    msg.attach(part1)

    if html:
        part2 = MIMEText(html, "html", "utf8")
        msg.attach(part2)


    server = smtplib.SMTP_SSL(host)
    server.login(login, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
    return True