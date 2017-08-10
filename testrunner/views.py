from django.shortcuts import render
from django.http import HttpResponse, Http404
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
from django.contrib.auth.models import User

# serializers
from testrunner.serializers import TestRunSerializer
from testrunner.serializers import TestRunInstanceSerializer
from testrunner.serializers import TestEnvironmentSerializer
from testrunner.serializers import UserSerializer

# forms
from testrunner.forms import TestRunInstanceForm, TestRunForm

def generate_test_suite_hiearchy(root):
    """
    Starting at `root` crawl the filesystem looking for:
        - directoryies containing files starting with test_
        - any file beginning with test_
    """

# views
@login_required
def create_instance(request):
    """
    Create and run an instance of a TestRun, or create a new TestRun
    first and then run an instance.
    """
    template = 'create_instance.html'

    # create queryset to hold all current testrun instances
    testruns = TestRunInstance.objects.all()

    if request.method == 'POST':
        instance_form = TestRunInstanceForm(request.POST)

        if instance_form.is_valid():
            form = instance_form.save(commit=False)
            form.requested_by = request.user
            form.save()
            # execute testrun instance...
    else:
        instance_form = TestRunInstanceForm(label_suffix=':')
        testrun_form = TestRunForm()

    context = {
        'form': instance_form,
        'trform': testrun_form,
        'testruns': testruns,
    }

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
