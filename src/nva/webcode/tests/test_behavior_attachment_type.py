# -*- coding: utf-8 -*-
from nva.webcode.behaviors.attachment_type import IAttachmentTypeMarker
from nva.webcode.testing import NVA_WEBCODE_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class AttachmentTypeIntegrationTest(unittest.TestCase):

    layer = NVA_WEBCODE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_attachment_type(self):
        behavior = getUtility(IBehavior, 'nva.webcode.attachment_type')
        self.assertEqual(
            behavior.marker,
            IAttachmentTypeMarker,
        )
