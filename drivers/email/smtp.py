from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from driver_class import EmailDriver
import os
import getpass

from drivers.render.html import HTMLTemplateRenderer


class SMTPMailDriver(EmailDriver):
    """
    SMTPMailDriver is a driver class that sends the rendered data to the email address.

    The password is not stored in the config file for obvious reasons. It will be read
    from the SMTP_PASSWORD environment variable, and if this is not present, a prompt
    will be shown to enter the password.
    """

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.password = os.getenv("SMTP_PASSWORD") or getpass.getpass(
            "Enter the password for your SMTP account: "
        )

    def send(self, data):
        """
        Send the rendered data to the email address.
        """
        config = self.config.get("smtp")
        if not config:
            self.logger.fatal("No SMTP configuration found.")
            exit(1)

        server = config["server"] or "localhost"
        port = config["port"] or 25
        sender = config["sender"]

        if not sender:
            self.logger.fatal("No sender email address found.")
            exit(1)

        self.logger.info(f"Connecting to SMTP server {server}:{port}")
        with smtplib.SMTP(server, port) as smtp:
            try:
                smtp.starttls()
                smtp.login(sender, self.password)
            except smtplib.SMTPAuthenticationError as err:
                self.logger.fatal(
                    "Authentication failed. Please double check your credentials."
                )
                exit(1)
            except smtplib.SMTPException as err:
                self.logger.fatal(
                    f"Could not connect to SMTP server {server}:{port}."
                    + f" Please double check your configuration."
                )
                exit(1)

            email_renderer = HTMLTemplateRenderer(self.config)
            rendered_html = email_renderer.render(data)

            rendered_html = email_renderer.render(data)

            message = MIMEMultipart()
            message["From"] = config.get("sender")
            message["To"] = data["Email"]
            message["Cc"] = ",".join(self.config.get("cc", ()))
            message[
                "Subject"
            ] = f"Report card for {self.config['generate']['exam_name']}"
            # attach pdf file
            with open(data["pdf_path"], "rb") as attachment:
                part = MIMEApplication(attachment.read(), "pdf")
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.split(data['pdf_path'])[-1]}",
                )
                message.attach(part)

            # attach filled template
            part = MIMEText(rendered_html, "html")
            message.attach(part)

            smtp.send_message(message, sender, message["To"])

            smtp.quit()
