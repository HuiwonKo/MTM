from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
]
