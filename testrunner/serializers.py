from rest_framework import serializers
from testrunner.models import TestRun, RESULT_CHOICES

class TestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRun
        fields = (
            'id',
            'name',
            'description',
            'last_run',
            'last_result',
            'created_on',
        )
