from django.urls import path
from authtools import views
import accounts.views

app_name = 'accounts'

urlpatterns = [
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('new_profile/', accounts.views.new_profile, name='new_profile'),
    path('update_profile/', accounts.views.update_profile, name='update_profile'),
    path('profile_page/', accounts.views.profile_page, name='profile_page'),
]
