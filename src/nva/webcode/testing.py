# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import nva.webcode


class NvaWebcodeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=nva.webcode)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'nva.webcode:default')


NVA_WEBCODE_FIXTURE = NvaWebcodeLayer()


NVA_WEBCODE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NVA_WEBCODE_FIXTURE,),
    name='NvaWebcodeLayer:IntegrationTesting',
)


NVA_WEBCODE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(NVA_WEBCODE_FIXTURE,),
    name='NvaWebcodeLayer:FunctionalTesting',
)


NVA_WEBCODE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        NVA_WEBCODE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='NvaWebcodeLayer:AcceptanceTesting',
)
