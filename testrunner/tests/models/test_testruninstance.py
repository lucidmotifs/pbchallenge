import os, time, sys, unittest
from django.test import TestCase
from testrunner.forms import TestRunInstanceForm, TestRunForm

import logging
logname = "testrunner.tests.models.{}".format(os.path.basename(__file__).replace(".py", ".log"))
logging.basicConfig(
    filename=logname,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG)

class InstanceTestCase(TestCase):
    def setUp(self):
        logging.info("Setting up")

    def tearDown(self):
        logging.info("Tearing down")

    def test_testrun_instance_fields(self):
        self.assertTrue(True)

    def test_dummy_pass(self):
        logging.info("We're passing")
        self.assertTrue(True)

    def test_dummy_exception(self):
        raise TypeError

    def test_dummy_delayed(self):
        logging.info("sleeping 1")
        time.sleep(1)

        self.assertTrue(True)
