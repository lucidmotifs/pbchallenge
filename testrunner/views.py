from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# REST API imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions

# app models
from testrunner.models import TestRun
from testrunner.models import TestRunInstance
from testrunner.models import TestEnvironment
from testrunner.models import TestModule
from django.contrib.auth.models import User

# serializers
from testrunner.serializers import TestRunSerializer
from testrunner.serializers import TestRunInstanceSerializer
from testrunner.serializers import TestEnvironmentSerializer
from testrunner.serializers import UserSerializer

# forms
from testrunner.forms import TestRunInstanceForm, TestRunForm

# utlities
from testrunner.helpers import create_hierarchy, get_test_modules

@login_required
def display_modules(request):
    """
    This is a temporary method while developing to help
    populate the TestModule DB from a filesystem. It would be
    protected and added to a control panel in prod. This code
    would move to a utlities module.
    """
    TestModule.objects.all().delete()
    # create the list to hold the TestModule list
    module_l = list()
    # get a list of test modules
    _tmodules = get_test_modules('/Users/paulcooper/Documents/GitHub/pbchallenge/testrunner/tests/')
    for m in _tmodules:
        module_l.append(TestModule(path=m))

    # create all modules in bulk, should purge first TODO
    TestModule.objects.bulk_create(module_l)

    tmodules = TestModule.objects.all()

    template = "testrunner/display_modules.html"
    context = {
        'modules':tmodules,
    }

    return render(request, template, context)

# views
@login_required
def create_testrun(request):
    """
    Parse the create_testrun form and save, then re-direct to the
    index screen.
    """
    if request.method == 'POST':
        testrun_form = TestRunForm(request.POST)

        # replace file name with pk of module


        if testrun_form.is_valid():
            form = testrun_form.save(commit=False)
            form.created_by = request.user
            form.save()
            testrun_form.save_m2m()            

            # get the last entered TestRun
            added = TestRun.objects.latest('id')

            # go to index
            return HttpResponseRedirect('/?tr={}'.format(added.id))
        else:
            # we should redirect to the index and pass a GET
            # variable to tell the user there was an error.
            # preferably open the form modal first and display.
            # return HttpResponseRedirect('/?errcode=1')
            template = "testrunner/form_errors.html"
            context = { 'form': testrun_form }
            return render(request, template, context)

    else:
        # immediately redirect the user, this page is only for
        # processing (with the goal of AJAXing the entire process.)
        return HttpResponseRedirect('/')


@login_required
def create_instance(request):
    """
    Create and run an instance of a TestRun, or create a new TestRun
    first and then run an instance.
    """
    context = {}
    template = 'testrunner/create_instance.html'

    # create queryset to hold all current testrun instances
    testruns = TestRunInstance.objects.all()

    # generate the test modules hierarchy
    tmodules = get_test_modules(
        '/Users/paulcooper/Documents/GitHub/pbchallenge/testrunner/tests')

    # build a nested dictionary hierarchy of the filesystem
    fs_hierarchy = create_hierarchy(tmodules)

    if request.method == 'POST':
        instance_form = TestRunInstanceForm(request.POST)
        testrun_form = TestRunForm(request.POST)

        if instance_form.is_valid():
            form = instance_form.save(commit=False)
            form.requested_by = request.user
            form.save()

            # assume save was successful...
            # TODO more defensive coding
            # pull the last entered instance
            testrun_instance = TestRunInstance.objects.latest('id')
            first_module = testrun_instance.testrun.modules.all()[0]
            context.update({
                'testrun_current':testrun_instance,
                'first_module':first_module
            })
    else:
        # set the initial to the passed in GET var, or just 0
        instance_form = TestRunInstanceForm(
            initial={'testrun': request.GET.get('tr', 0)},
            label_suffix=':')

        # create a testrun_form for the 'add new' modal
        testrun_form = TestRunForm()

        # add the forms to page context
        context.update({
            'form': instance_form,
            'trform': testrun_form,
        })

    context.update({
        'testruns': testruns,
        'files': fs_hierarchy,
    })

    return render(request, template, context)


class TestRunList(APIView):
    """
    List all available test runs, or create a new test run.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TestRunSerializer

    def get(self, request, format=None):
        testruns = TestRun.objects.all()
        serializer = TestRunSerializer(testruns, many=True)

        return Response(serializer.data)


    def post(self, request, format=None):
        serializer = TestRunSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=self.request.user)

            return Response(serializer.data, \
                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, \
            status=status.HTTP_400_BAD_REQUEST)


class TestRunDetail(APIView):
    """
    Retrieve, update or delete a test run.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TestRunSerializer


    def get_testrun(self, pk):
        try:
            return TestRun.objects.get(pk=pk)
        except TestRun.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        testrun = self.get_testrun(pk)
        serializer = TestRunSerializer(testrun)

        return Response(serializer.data)


    def put(self, request, pk, format=None):
        testrun = self.get_testrun(pk)
        serializer = TestRunSerializer(testrun, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, \
            status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        testrun = self.get_testrun(pk)
        testrun.delete() # TODO what happens to child instances?

        return Response(status=status.HTTP_204_NO_CONTENT)


class TestEnvironmentList(generics.ListCreateAPIView):
    queryset = TestEnvironment.objects.all()
    serializer_class = TestEnvironmentSerializer


class TestEnvironmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestEnvironment.objects.all()
    serializer_class = TestEnvironmentSerializer


class TestRunInstanceList(generics.ListCreateAPIView):
    queryset = TestRunInstance.objects.all()
    serializer_class = TestRunInstanceSerializer

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)


class TestRunInstanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestRunInstance.objects.all()
    serializer_class = TestRunInstanceSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
