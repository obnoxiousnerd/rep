import smtplib

port = 1025
smtp_server = "localhost"
sender_email = "me@localhost"  # Enter your address
receiver_email = "you@localhost"  # Enter receiver address
username = "repcli"
password = "12345678"
message = """\
Subject: Hi there

This message is sent from Python."""

server = smtplib.SMTP("localhost", port)
server.starttls()
server.login(username, password)
server.set_debuglevel(True)

try:
    server.sendmail(sender_email, [receiver_email], message)
finally:
    server.quit()
