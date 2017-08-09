from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from testrunner import views

urlpatterns = [
    url(r'^testruns/$', views.testrun_list),
    url(r'^testruns/(?P<pk>[0-9]+)/$', views.testrun_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
