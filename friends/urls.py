from django.conf.urls import url
from . import views
from django.urls import include, path


app_name = "friends"

urlpatterns = [
    url(r'^friends_posts_list/$', views.friends_posts_list, name='friends_posts_list'),
    url(r'^friends_posts_list/(?P<user>\w+)/$', views.individual_friend_post_list,
        name='individual_friend_post_list'),
    url(r'^private_posts_list/$', views.private_posts_list, name='private_posts_list'),
]