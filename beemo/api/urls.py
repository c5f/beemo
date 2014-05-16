from django.conf.urls import patterns, include, url

from api import views

urlpatterns = patterns('',

    url(r'^participants/$', views.ParticipantList.as_view()),
    url(r'^participants/(?P<pk>[0-9]+)/$', views.ParticipantDetail.as_view()),

    url(r'^calls/$', views.CallList.as_view()),
    url(r'^calls/(?P<pk>[0-9]+)/$', views.CallDetail.as_view())

)
