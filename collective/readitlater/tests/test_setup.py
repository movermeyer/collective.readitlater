import unittest2 as unittest
from collective.readitlater.tests import base


class TestSetup(base.IntegrationTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """

    def test_browserlayer(self):
        from plone.browserlayer import utils
        from collective.readitlater import layer
        self.assertIn(layer.Layer, utils.registered_layers())

    def test_controlpanel(self):
        pass

    def test_registry(self):
        pass


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
