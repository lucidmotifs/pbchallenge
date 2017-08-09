from django.shortcuts import render
from django.http import HttpResponse, Http404

# REST API imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions

# app models
from testrunner.models import TestRun
from django.contrib.auth.models import User

# serializers
from testrunner.serializers import TestRunSerializer
from testrunner.serializers import UserSerializer

# views
class TestRunList(APIView):
    """
    List all available test runs, or create a new test run.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


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

"""
If no more logic is required, use this instead:
...
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
"""

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
