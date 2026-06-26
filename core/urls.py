from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('weather/', views.weather, name='weather'),
    path('api/weather/', views.weather_api, name='weather_api'),
    path('resources/', views.resources, name='resources'),
    path('news/', views.news_list, name='news'),
    path('alerts/', views.alerts_list, name='alerts'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('monitor/', views.monitor, name='monitor'),
    path('monitor/export/audits.csv', views.export_audits_csv, name='export_audits_csv'),
    path('monitor/export/weather.csv', views.export_weather_csv, name='export_weather_csv'),
    path('monitor/data.json', views.monitor_data, name='monitor_data'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
