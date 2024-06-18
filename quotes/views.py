from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User  # Добавьте этот импорт
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from .forms import UserRegisterForm, AuthorForm, QuoteForm, CustomPasswordResetForm
from .models import Author, Quote
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('quotes-home')
    else:
        form = UserRegisterForm()
    return render(request, 'quotes/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('quotes-home')
    else:
        form = AuthenticationForm()
    return render(request, 'quotes/login.html', {'form': form})
@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes-home')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return redirect('quotes-home')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

def home(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/home.html', {'quotes': quotes})

def author_detail(request, pk):
    author = Author.objects.get(pk=pk)
    quotes = Quote.objects.filter(author=author)
    return render(request, 'quotes/author_detail.html', {'author': author, 'quotes': quotes})

def send_email(subject, body, recipient_list):
    try:
        smtp_host = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        sender_email = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD

        # Создаем объект SMTP
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # Начинаем шифрованное соединение

        # Аутентификация на сервере SMTP
        server.login(sender_email, password)

        # Создаем сообщение
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = ', '.join(recipient_list)
        message['Subject'] = subject

        # Текст письма
        message.attach(MIMEText(body, 'plain'))

        # Отправляем сообщение
        server.sendmail(sender_email, recipient_list, message.as_string())

        print('Email sent successfully!')

        # Закрываем соединение с сервером
        server.quit()

    except Exception as e:
        print(f'Error sending email: {e}')
        messages.error(request, f'Error sending email: {e}')

def send_test_email(request):
    subject = "Test Email from Python"
    body = "This is a test email sent from Python."
    recipient_list = ['kiril4a.mvdk@gmail.com']  # Замените на адрес получателя
    send_email(subject, body, recipient_list)
    messages.success(request, 'Test email sent successfully.')
    return redirect('login')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = CustomPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',  # ваш домен
                        'site_name': 'your site',  # имя вашего сайта
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',  # или 'https' если это SSL
                    }
                    email = render_to_string(email_template_name, c)

                    # Отправляем email с помощью нашей функции send_email()
                    send_email(subject, email, [user.email])

                    # Выводим сообщение об успешной отправке или об ошибке, если таковая произошла
                    messages.success(request, 'Email sent successfully.')
                    return render(request, 'registration/password_reset_done.html')

    # Если форма не валидна или пользователь с таким email не найден, просто возвращаем форму снова
    password_reset_form = CustomPasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': password_reset_form})
