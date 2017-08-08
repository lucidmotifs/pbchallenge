from rest_framework import serializers
from testrunner.models import TestRun, RESULT_CHOICES

class TestRunSerialiazer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, blank=True, max_length=100)
    description = serializers.CharField(
        required=False,
        blank=True,
        max_length=200
    )
    last_result = serializers.CharField(
        choices=RESULT_CHOICES,
        default='Null',
        max_length=20
    )


    def create(self, validated_data):
        """
        Create and return a new `TestRun` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `TestRun` instance, given the
        validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', \
            instance.description)
        # TODO add ability 
        instance.save()
        return instance
