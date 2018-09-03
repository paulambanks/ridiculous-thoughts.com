from django.urls import path
from authtools import views
import accounts.views
from django.conf.urls import url

app_name = 'accounts'

urlpatterns = [
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile_page/', accounts.views.profile_page, name='profile_page'),
    url(r'^edit_user/(?P<pk>[\-\w]+)/$', accounts.views.edit_user, name='edit_user'),

]