from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='quotes-home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='login'),
    path('add_author/', views.add_author, name='add-author'),
    path('add_quote/', views.add_quote, name='add-quote'),
    path('author/<int:pk>/', views.author_detail, name='author-detail'),
    # URL для сброса пароля
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    # URL для отправки тестового email
    path('send_test_email/', views.send_test_email, name='send_test_email'),

    
]
