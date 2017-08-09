from rest_framework import serializers
from testrunner.models import TestRun, RESULT_CHOICES
from django.contrib.auth.models import User

class TestRunSerializer(serializers.ModelSerializer):
    """
    Serializer for the TestRun model
    """

    created_by = serializers.ReadOnlyField(source='created_by.username')

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
