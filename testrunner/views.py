from django.shortcuts import render
from django.http import HttpResponse

# REST API imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# app models
from testrunner.models import TestRun

# serializers
from testrunner.serializers import TestRunSerializer

# views
@api_view(['GET', 'POST'])
def testrun_list(request, format=None):
    """
    List all available test runs, or create a new test run.
    """
    if request.method == 'GET':
        testruns = TestRun.objects.all()
        serializer = TestRunSerializer(testruns, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TestRunSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, \
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, \
            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def testrun_detail(request, pk, format=None):
    """
    Retrieve, update or delete a test run.
    """
    try:
        testrun = TestRun.objects.get(pk=pk)
    except TestRun.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TestRunSerializer(testrun)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TestRunSerializer(testrun, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, \
            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        testrun.delete() # TODO what happens to child instances?
        return Response(status=status.HTTP_204_NO_CONTENT)
