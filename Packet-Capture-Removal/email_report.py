import smtplib

from email.mime.text import MIMEText

def send_email_report(message_body):
    from_addr = "test_email@address.com"
    to_addrs = ["to@address.com", "other@address.com"]
    mail_server = 'x.x.x.x'

    subject = "Daily Packet Capture Report"
    msg = MIMEText(message_body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    for to_count in range(len(to_addrs)):
        msg['To'] = to_addrs[to_count]
        server = smtplib.SMTP(mail_server, 25)
        server.sendmail(from_addr, [to_addrs[to_count]], msg.as_string())
