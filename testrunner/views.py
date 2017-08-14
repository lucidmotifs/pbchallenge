import json, os, re
from datetime import datetime

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
from testrunner.forms import TestRunInstanceForm, TestRunForm, TestEnvironmentForm

# utlities
from testrunner.helpers import create_hierarchy, get_test_modules, execute_test_django
from testrunner.helpers import TESTS_DIR

@login_required
def get_logs(request):

    if request.method == 'GET':
        iid = request.GET.get('instance_id')

        instance = TestRunInstance.objects.filter(id=iid)[0]
        response_data = {}
        response_data['logs_content'] = ""
        for m in instance.testrun.modules.all():
            # HACK fix module path at POST
            m.path = m.path.replace('./', '')
            dir = "{}logs/{}/".format(TESTS_DIR, iid)
            filename = "{}{}".format(TESTS_DIR, m.path)
            # make replacements to match logfile name on disk
            filename = filename.replace('/', '.')
            filename = filename.replace('.py', '.log')
            filename = dir + filename
            # open log file and return contents
            with open(filename, 'r') as log_file:
                response_data['logs_content'] += log_file.read()

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"error": "error"}),
            content_type="application/json"
        )

# views
@login_required
def execute_test(request):
    """
    This view is designed to take a POST request and return a
    JSON response after executing the posted test module.

    Time allowing, we would put this into an APIView class so the testrunner
    code doesn't live in helpers.py
    """
    if request.method == 'POST':

        module_id = request.POST.get('m_id')
        instance_id = request.POST.get('run_id')

        # the dictionary to be JSON encoded
        response_data = {}

        # use the posted ID to pull the test module
        module = TestModule.objects.filter(id=module_id)[0]

        # send the path to the helper that actually runs the test
        response_data['output'] = execute_test_django(module.path, instance_id)
        response_data['pk'] = module.id
        response_data['path'] = module.path

        # find the result. a single fail means the run fails
        output = response_data['output']

        # find all before the first newline
        m = re.search(r"(.*)\n", output, re.M)
        if m and ('F' in m.group(1) or 'E' in m.group(1)):
            response_data['result'] = 'FAILED'
        else:
            response_data['result'] = 'PASSED'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"error": "error"}),
            content_type="application/json"
        )


@login_required
def update_modules(request):
    """
    This is a temporary method while developing to help
    populate the TestModule DB from a filesystem. It would be
    protected and added to a control panel in prod. This code
    would move to a utlities module.
    """
    #TestModule.objects.all().delete()
    # create the list to hold the TestModule list
    module_l = list()
    # get a list of test modules
    _tmodules = get_test_modules('testrunner/tests/')
    for m in _tmodules:
        module_l.append(TestModule(path=m))

    # create all modules in bulk, should purge first TODO
    TestModule.objects.bulk_create(module_l)

    tmodules = TestModule.objects.all()

    template = "testrunner/update_modules.html"
    context = {
        'modules':tmodules,
    }

    return render(request, template, context)

@login_required
def display_testruni(request, pk):
    """
    Display and run a single testrun instance.
    """
    context = {}
    template = 'testrunner/display_testruni.html'

    # create queryset to hold all current testrun instances
    testrun_instance = TestRunInstance.objects.filter(id=pk)[0]
    modules = testrun_instance.testrun.modules.all()

    if request.method == 'POST':
        # updated the model with the test run result
        testrun_instance.output = request.POST.get('instance_output')
        testrun_instance.executed_on = datetime.now()

        # iterate through the attached modules and check their
        # result. If one fails, the run fails
        mids = list()
        for m in modules:
            field_id = "test-module--{}".format(m.id)
            mids.append(m.id)
            if request.POST.get(field_id) == 'FAILED':
                # break out, as a single failure means the run fails
                testrun_instance.result = 'FAILED'
                break
            else:
                testrun_instance.result = 'PASSED'
        context.update({'mids':mids})
        testrun_instance.save()

    # create queryset to hold all current testrun instances
    testruns = TestRunInstance.objects.all()

    context.update({
        'testrun_current': testrun_instance,
        'modules': modules,
        'testruns': testruns,
    })

    return render(request, template, context)

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

    Also, display previous test run results.
    """
    context = {}
    template = 'testrunner/create_instance.html'

    # create queryset to hold all current testrun instances
    testruns = TestRunInstance.objects.all()

    # instance of the TestEnvironmentForm for our modal
    testenv_form = TestEnvironmentForm(request.POST)

    # generate the test modules hierarchy
    tmodules = get_test_modules('testrunner/tests')

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
            modules = testrun_instance.testrun.modules.all()
            context.update({
                'testrun_current':testrun_instance,
                'modules':modules,
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
            'teform': testenv_form,
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TestEnvironmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestEnvironment.objects.all()
    serializer_class = TestEnvironmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


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
