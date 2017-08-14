from django.conf.urls import url
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns

# app views
from testrunner import views

urlpatterns = [
    url(r'^$', views.create_instance),
    url(r'^create_testrun/', views.create_testrun, name="index"),
    url(r'^run/(?P<pk>[0-9]+)/$', views.display_testruni, name="display-instance"),
    url(r'^update_modules/', views.update_modules),
    url(r'^api/exec_test/', views.execute_test),
    url(r'^api/logs/', views.get_logs),
    url(r'^api/testruns/$', views.TestRunList.as_view(), name="api-testruns"),
    url(r'^api/testruns/(?P<pk>[0-9]+)/$', views.TestRunDetail.as_view()),
    url(r'^api/envs/$', views.TestEnvironmentList.as_view(), name='api-envs'),
    url(r'^api/envs/(?P<pk>[0-9]+)/$', views.TestEnvironmentDetail.as_view()),
    url(r'^api/runs/$', views.TestRunInstanceList.as_view(), name="api-instances"),
    url(r'^api/runs/(?P<pk>[0-9]+)/$', views.TestRunInstanceDetail.as_view()),
    url(r'^api/users/$', views.UserList.as_view(), name="api-users"),
    url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
