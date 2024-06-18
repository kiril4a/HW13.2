import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from quotes_project import settings

def send_test_email():
    try:
        smtp_host = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        sender_email = settings.EMAIL_HOST_USER
        receiver_email = 'kiril4a.mvdk@gmail.com'  # Замените на адрес получателя
        password = settings.EMAIL_HOST_PASSWORD

        # Создаем объект SMTP
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # Начинаем шифрованное соединение

        # Аутентификация на сервере SMTP
        server.login(sender_email, password)

        # Создаем сообщение
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = 'Test Email from Python'

        # Текст письма
        body = 'This is a test email sent from Python.'
        message.attach(MIMEText(body, 'plain'))

        # Отправляем сообщение
        server.sendmail(sender_email, receiver_email, message.as_string())

        print('Email sent successfully!')

        # Закрываем соединение с сервером
        server.quit()

    except Exception as e:
        print(f'Error sending email: {e}')

# Вызываем функцию для отправки тестового email
send_test_email()
