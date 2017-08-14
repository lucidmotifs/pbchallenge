import time, sys, unittest
from django.test import TestCase
from testrunner.forms import TestRunInstanceForm, TestRunForm

class StaticTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_testrun_instance_fields(self):
        time.sleep(2)
        self.assertTrue(True)

    def test_dummy_pass(self):
        self.assertTrue(1 == 1)

    def test_dummy_delayed(self):
        time.sleep(12)

        self.assertTrue(True)
