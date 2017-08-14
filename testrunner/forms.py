from django import forms
from django.forms import ModelForm
from testrunner.models import TestRunInstance, TestRun, TestModule, TestEnvironment


class TestRunInstanceForm(ModelForm):
    class Meta:
        model = TestRunInstance
        fields = ['testrun', 'interface', 'environment']


class TestEnvironmentForm(ModelForm):
    class Meta:
        model = TestEnvironment
        fields = ['host']


class TestRunForm(ModelForm):
    # Representing the many to many related field in TestRun
    modules = forms.ModelMultipleChoiceField(queryset=TestModule.objects.all())

    class Meta:
        model = TestRun
        fields = ['name', 'description', 'modules']
