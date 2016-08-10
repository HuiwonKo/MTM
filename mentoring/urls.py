from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static


from . import views

urlpatterns = [
    url(r'^mentor/list/$', views.mentor_list, name='mentor_list'),
    url(r'^mentor/(?P<pk>\d+)/$', views.post_by_mentor_detail, name='post_by_mentor_detail'),
    url(r'^mentor/new/$', views.post_by_mentor_new, name='post_by_mentor_new'),
    url(r'^mentor/(?P<pk>\d+)/edit/$', views.post_by_mentor_edit, name='post_by_mentor_edit'),
    url(r'^mentor/(?P<pk>\d+)/delete/$', views.post_by_mentor_delete, name='post_by_mentor_delete'),
    url(r'^mentor/(?P<post_pk>\d+)/bid/(?P<pk>\d+)/$', views.bid_by_mentee_detail, name='bid_by_mentee_detail'),
    url(r'^mentor/(?P<post_pk>\d+)/bid/new/$', views.bid_by_mentee_new, name='bid_by_mentee_new'),
    url(r'^mentor/(?P<post_pk>\d+)/bid/(?P<pk>\d+)/edit/$', views.bid_by_mentee_edit, name='bid_by_mentee_edit'),
    url(r'^mentor/(?P<post_pk>\d+)/bid/(?P<pk>\d+)/delete/$', views.bid_by_mentee_delete, name='bid_by_mentee_delete'),
    url(r'^mentor/(?P<post_pk>\d+)/comment/new/$', views.comment_new, name='comment_new'),
    url(r'^mentor/(?P<post_pk>\d+)/comment/(?P<pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
    url(r'^mentor/(?P<post_pk>\d+)/comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),

    url(r'^mentee/list/$', views.mentee_list, name='mentee_list'),
    url(r'^mentee/(?P<pk>\d+)/$', views.post_by_mentee_detail, name='post_by_mentee_detail'),
    url(r'^mentee/new/$', views.post_by_mentee_new, name='post_by_mentee_new'),
    url(r'^mentee/(?P<pk>\d+)/edit/$', views.post_by_mentee_edit, name='post_by_mentee_edit'),
    url(r'^mentee/(?P<pk>\d+)/delete/$', views.post_by_mentee_delete, name='post_by_mentee_delete'),
    url(r'^mentee/(?P<post_pk>\d+)/bid/(?P<pk>\d+)/$', views.bid_by_mentor_detail, name='bid_by_mentor_detail'),
    url(r'^mentee/(?P<post_pk>\d+)/bid/new/$', views.bid_by_mentor_new, name='bid_by_mentor_new'),
    url(r'^mentee/(?P<post_pk>\d+)/bid/(?P<pk>\d+)/edit/$', views.bid_by_mentor_edit, name='bid_by_mentor_edit'),
    url(r'^mentee/(?P<post_pk>\d+)/bid/(?P<pk>\d+)/delete/$', views.bid_by_mentor_delete, name='bid_by_mentor_delete'),
    url(r'^mentee/(?P<post_pk>\d+)/bid/(?P<pk>\d+)/match/$', views.matched_bid_by_mentor, name='matched_bid_by_mentor'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
