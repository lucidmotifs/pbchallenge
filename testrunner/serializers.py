from rest_framework import serializers
from testrunner.models import TestRun, TestEnvironment, TestRunInstance
from testrunner.models import RESULT_CHOICES
from django.contrib.auth.models import User

class TestRunSerializer(serializers.ModelSerializer):
    """
    Serializer for the TestRun model
    """

    created_by = serializers.ReadOnlyField(source='created_by.username')
    created_on = serializers.ReadOnlyField()

    class Meta:
        model = TestRun
        fields = (
            'id',
            'name',
            'description',
            'last_run',
            'last_result',
            'created_on',
            'created_by',
        )


class TestEnvironmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Environment model.
    """

    class Meta:
        model = TestEnvironment
        fields = '__all__'


class TestRunInstanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the TestRunInstance model.
    """

    requested_by = serializers.ReadOnlyField(
        source='requested_by.username')
    created_on = serializers.ReadOnlyField()
    executed_on = serializers.ReadOnlyField()
    output = serializers.ReadOnlyField()
    result = serializers.ReadOnlyField()

    class Meta:
        model = TestRunInstance
        fields = (
            'id',
            'testrun',
            'requested_by',
            'interface',
            'environment',
            'result',
            'output',
            'executed_on',
            'created_on',
        )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django built in User model.
    """

    testruns = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TestRun.objects.all()
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'testruns')
