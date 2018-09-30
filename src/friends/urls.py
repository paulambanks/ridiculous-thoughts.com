from django.conf.urls import url
from . import views


app_name = "friends"

urlpatterns = [
    url(r'^friends_posts_list/$', views.friends_posts_list, name='friends_posts_list'),
    url(r'^private_posts_list/$', views.private_posts_list, name='private_posts_list'),

]
