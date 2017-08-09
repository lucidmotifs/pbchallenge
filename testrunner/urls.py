from django.conf.urls import url
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns

# app views
from testrunner import views

urlpatterns = [
    url(r'^testruns/$', views.TestRunList.as_view()),
    url(r'^testruns/(?P<pk>[0-9]+)/$', views.TestRunDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
