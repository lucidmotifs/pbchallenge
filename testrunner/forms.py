from django import forms
from django.forms import ModelForm
from testrunner.models import TestRunInstance, TestRun, TestModule


class TestRunInstanceForm(ModelForm):
    class Meta:
        model = TestRunInstance
        fields = ['testrun', 'interface', 'environment']


class TestRunForm(ModelForm):
    # Representing the many to many related field in TestRun
    modules = forms.ModelMultipleChoiceField(queryset=TestModule.objects.all())

    class Meta:
        model = TestRun
        fields = ['name', 'description', 'modules']

    # overriding to handle the ManyToManyField modules
    def __save(self, commit=True):
        # Get the unsave TestRun instance
        instance = ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        sup_savem2m = self.save_m2m
        def save_m2m():
           sup_savem2m()
           # This is where we actually link the testrun with modules
           instance.modules_set.clear()
           for module in self.cleaned_data['modules']:
               instance.modules_set.add(module)

        self.save_m2m = sup_savem2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance
