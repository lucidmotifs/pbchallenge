from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

INTERFACE_CHOICES = (
    ('ssh', 'ssh'),
    ('lfs', 'local'),
)

RESULT_CHOICES = (
    ('pass', 'pass'),
    ('fail', 'fail'),
    ('error', 'error'),
)

# Create your models here.
class TestEnvironment(models.Model):
    host = models.CharField(max_length=100, default='localhost')


class TestRun(models.Model):
    """ A model that can be requested to create a testrun instance. """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True)

    """
    The below attributes should only be set by the system after a
    TestRunInstance completes
    """

    last_run = models.DateTimeField(null=True)
    last_result = models.CharField(
        choices=RESULT_CHOICES,
        max_length=20,
        null=True
    )

    created_by = models.ForeignKey(User, null=True)
    created_on = models.DateTimeField(default=datetime.now)
    # Tests are linked to TestRun via ForeignKey relationships


class TestRunInstance(models.Model):
    """ Instance of a TestRun that has or will be executed """
    requester = models.ForeignKey(User)

    interface = models.CharField(
        choices=INTERFACE_CHOICES,
        default='ssh',
        max_length=20
    )

    environment = models.ForeignKey(TestEnvironment)

    created_on = models.DateTimeField()
    executed_on = models.DateTimeField()

    class Meta:
        ordering = ('created_on',)


class Template(models.Model):
    """ A collection of tests. When attached to a TestRun, adds each Test
    individually. Exists for convenience """
    pass


class TestModule(models.Model):
    """ A reference to a file that contains one or more tests and exists
    the specified testing directory. """
    pass
