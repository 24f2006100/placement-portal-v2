import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_ADDRESS = "SENDERS_EMAIL"
EMAIL_PASSWORD = "16_character_app_password"

def send_email(
    to_email,
    subject,
    body,
    html=False
):

    message = MIMEMultipart()

    message["From"] = EMAIL_ADDRESS
    message["To"] = to_email
    message["Subject"] = subject

    content_type = (
        "html"
        if html
        else "plain"
    )

    message.attach(
        MIMEText(
            body,
            content_type
        )
    )

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.send_message(message)


    print( f"Email sent successfully to {to_email}")