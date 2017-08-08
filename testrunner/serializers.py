from rest_framework import serializers
from testrunner.models import TestRun, RESULT_CHOICES

class TestRunSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100)
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=200
    )
    last_result = serializers.ChoiceField(
        choices=RESULT_CHOICES,
        default='never_run',
    )


    def create(self, validated_data):
        """
        Create and return a new `TestRun` instance, given the validated data.
        """
        return TestRun.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `TestRun` instance, given the
        validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', \
            instance.description)
        # TODO add ability to update and change attached tests.
        # ...more
        instance.save()
        return instance
