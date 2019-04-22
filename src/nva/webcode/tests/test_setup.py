# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from nva.webcode.testing import NVA_WEBCODE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


no_get_installer = False


try:
    from Products.CMFPlone.utils import get_installer
except Exception:
    no_get_installer = True


class TestSetup(unittest.TestCase):
    """Test that nva.webcode is properly installed."""

    layer = NVA_WEBCODE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])

    def test_product_installed(self):
        """Test if nva.webcode is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'nva.webcode'))

    def test_browserlayer(self):
        """Test that INvaWebcodeLayer is registered."""
        from nva.webcode.interfaces import (
            INvaWebcodeLayer)
        from plone.browserlayer import utils
        self.assertIn(
            INvaWebcodeLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = NVA_WEBCODE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('nva.webcode')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if nva.webcode is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'nva.webcode'))

    def test_browserlayer_removed(self):
        """Test that INvaWebcodeLayer is removed."""
        from nva.webcode.interfaces import \
            INvaWebcodeLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            INvaWebcodeLayer,
            utils.registered_layers())
