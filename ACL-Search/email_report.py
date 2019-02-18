import smtplib

from email.mime.text import MIMEText


def build_message():
    f1 = open("Subnet-1-Results.txt", "r")
    txt1 = f1.read()
    f2 = open("Subnet-2-Results.txt", "r")
    txt2 = f2.read()
    f3 = open("Subnet-3-Results.txt", "r")
    txt3 = f3.read()
    email_message = ("Your Access-List search has been completed here are the results: \n")
    email_message += txt1 + "\n"
    email_message += txt2 + "\n"
    email_message += txt3 + "\n"
    send_email_report(email_message)


def send_email_report(message_body):
    from_addr = "test_email@address.com"
    to_addrs = ["to@address.com", "other@address.com"]
    mail_server = 'x.x.x.x'

    subject = "Access-List Search Results"
    msg= MIMEText(message_body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    for to_count in range(len(to_addrs)):
        msg['To'] = to_addrs[to_count]
        server = smtplib.SMTP(mail_server, 25)
        server.sendmail(from_addr, [to_addrs[to_count]], msg.as_string())


