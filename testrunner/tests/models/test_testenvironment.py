import time, sys, unittest
from django.test import TestCase
from testrunner.forms import TestRunInstanceForm, TestRunForm

class EnvironmentTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_testrun_unique_environment(self):
        time.sleep(10)
        self.assertTrue(True)

    def test_dummy_delayed(self):
        time.sleep(20)
        self.assertTrue(True)
