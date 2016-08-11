from django.conf.urls import url
from django.contrib.auth.views import login

from . import views


urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$',logout, name='logout'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
    url(r'^mentor_info/$', views.mentor_info, name='mentor_info'),
    url(r'mentor_info_edit/$', views.mentor_info_edit, name='mentor_info_edit'),
    url(r'^matched_list/$', views.matched_list, name='matched_list'),
   ]
