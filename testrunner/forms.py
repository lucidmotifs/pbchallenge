from django.forms import ModelForm
from testrunner.models import TestRunInstance, TestRun


class TestRunInstanceForm(ModelForm):
    class Meta:
        model = TestRunInstance
        fields = ['testrun', 'interface', 'environment']


class TestRunForm(ModelForm):
    class Meta:
        model = TestRun
        fields = ['name', 'description', 'modules']
