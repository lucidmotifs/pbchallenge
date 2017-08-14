from django.conf.urls import url
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns

# app views
from testrunner import views

urlpatterns = [
    url(r'^$', views.create_instance),
    url(r'^create_testrun/', views.create_testrun),
    url(r'^run/(?P<pk>[0-9]+)/$', views.display_testruni, name="display-instance"),
    url(r'^display_modules/', views.display_modules),
    url(r'^api/exec_test/', views.execute_test_ajax),
    url(r'^api/testruns/$', views.TestRunList.as_view()),
    url(r'^api/testruns/(?P<pk>[0-9]+)/$', views.TestRunDetail.as_view()),
    url(r'^api/envs/$', views.TestEnvironmentList.as_view()),
    url(r'^api/envs/(?P<pk>[0-9]+)/$', views.TestEnvironmentDetail.as_view()),
    url(r'^api/runs/$', views.TestRunInstanceList.as_view()),
    url(r'^api/runs/(?P<pk>[0-9]+)/$', views.TestRunInstanceDetail.as_view()),
    url(r'^api/users/$', views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
