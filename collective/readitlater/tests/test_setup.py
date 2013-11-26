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

    def test_upgrades(self):
        profile = 'collective.readitlater:default'
        setup = self.portal.portal_setup
        upgrades = setup.listUpgrades(profile, show_old=True)
        self.assertTrue(len(upgrades) > 0)
        for upgrade in upgrades:
            upgrade['step'].doStep(setup)

    def test_vocabulary(self):
        from collective.readitlater.vocabulary import contentVocabulary
        vocabulary = contentVocabulary(self.portal)
        terms = vocabulary._terms
        self.assertEqual(len(terms), 1)
        term = terms[0]
        folder = getattr(self.portal, 'test-folder')
        self.assertEqual(term.title, folder.Title())
        self.assertEqual(term.token, folder.UID())
        self.assertEqual(term.value, folder.UID())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
