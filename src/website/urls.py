from django.conf.urls import url
from . import views
from django.urls import include, path


app_name = "website"

urlpatterns = [
    url(r'^$', views.posts_list, name="posts_list"),
    url(r'^post_list/$', views.posts_list, name='posts_list'),
    url(r'^tagged_posts_list/(?P<tag_id>\w+)/$', views.tagged_posts_list, name='tagged_posts_list'),
    url(r'^individual_author_posts/(?P<user>\w+)/$', views.individual_author_posts,
        name='individual_author_posts'),
    url(r'^shared_post_list/$', views.shared_post_list,
        name='shared_post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^shared_post/(?P<id>\d+)/$', views.shared_post_detail, name='shared_post_detail'),
    url(r'^post/new/$', views.post_form, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_form, name='post_edit'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/share/$', views.post_share, name='post_share'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^about/$', views.about, name='about'),
    path('accounts/', include('accounts.urls')),
    path('email/', views.send_email, name='email'),
    path('success/', views.email_success, name='success'),
    path('error/', views.error, name='error'),
]