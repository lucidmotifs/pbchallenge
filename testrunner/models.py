from datetime import datetime

from django.db import models

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

    def __str__(self):
        return "id: {}, host: {}".format(self.id, self.host)


class TestModule(models.Model):
    """ A reference to a file that contains one or more tests and exists
    the specified testing directory. """

    path = models.CharField(max_length=100)

    result = models.CharField(  choices=RESULT_CHOICES,
                                max_length=20,
                                null=True )


class TestRun(models.Model):
    """
    A model to be used as a launch point to create a testrun instance.
    """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True)
    modules = models.ManyToManyField(TestModule)

    """
    The below attributes should only be set by the system after a child
    TestRunInstance completes
    """

    last_run = models.DateTimeField(null=True)

    last_result = models.CharField( choices=RESULT_CHOICES,
                                    max_length=20,
                                    null=True )

    created_by = models.ForeignKey( 'auth.User',
                                    related_name='testruns',
                                    on_delete=models.CASCADE,
                                    null=False )
    created_on = models.DateTimeField(default=datetime.now)


    def save(self, *args, **kwargs):
        """
        Extra steps to perform before the object is saved to the DB
        """
        super(TestRun, self).save(*args, **kwargs)


    def __str__(self):
        return self.name


class TestRunInstance(models.Model):
    """ Instance of a TestRun that has or will be executed """
    requested_by = models.ForeignKey('auth.User', blank=True, null=True)

    testrun = models.ForeignKey(TestRun)

    interface = models.CharField( choices=INTERFACE_CHOICES,
                                  default='ssh',
                                  max_length=20 )

    environment = models.ForeignKey(TestEnvironment)

    result = models.CharField(  choices=RESULT_CHOICES,
                                max_length=20,
                                null=True )

    output = models.CharField(max_length=255, null=True)

    executed_on = models.DateTimeField(null=True)

    created_on = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ('-created_on', 'executed_on')


class Template(models.Model):
    """ A collection of tests. When attached to a TestRun, adds each Test
    individually. Exists for convenience """
    label = models.CharField(max_length=40, unique=True, null=False)
    modules = models.ManyToManyField(TestModule)
