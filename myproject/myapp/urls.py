# myproject/myapp/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignupView, LoginView, DashboardView, SetPinView, ChangePinView, FetchDataView, UnlockView, RequestPasswordResetView, ResetPasswordView, LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('set-pin/', SetPinView.as_view(), name='set_pin'),
    path('change-pin/', ChangePinView.as_view(), name='change_pin'),
    path('unlock/', UnlockView.as_view(), name='unlock'),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('fetch-data/', FetchDataView.as_view(), name='fetch_data'),

]