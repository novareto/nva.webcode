# -*- coding: utf-8 -*-
from DateTime import DateTime
import random
from nva.webcode import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model, directives
from zope.component import adapter
from zope.interface import Interface
from zope.interface import alsoProvides, implementer
from zope.interface import provider
from plone import api as ploneapi

def createWebcode():
    """ Dieser Event wird immer dann aufgerufen wenn ein Dokument modifiziert wird.
        Mit dem Event soll eine 8-stellige, moeglichst eindeutige Zahl gebildet werden. Das
        soll durch folgende Methode erreicht werden:
        * Verkettung 2-stellige Jahreszahl(Konstante) + 6-stellige Zufallszahl
        * Catalogabfrage, ob im betr. Jahr ein Objekt mit dieser Kombination vorhanden ist, wenn ja:
          * wiederholter Aufruf des Zusfallszahlengenerators
    """
    #Bildung des Webcodes
    aktuell=str(DateTime()).split(' ')[0]
    neujahr='%s/01/01' %str(DateTime()).split(' ')[0][:4]
    konstante=str(aktuell[2:4])
    zufallszahl=str(random.randint(100000, 999999))
    code=konstante+zufallszahl
    #Sicherheitsabfrage
    results =  ploneapi.content.find(Webcode=code)
    while results:
        zufallszahl=str(random.randint(100000, 999999))
        code=konstante+zufallszahl
        results =  ploneapi.content.find(Webcode=code)
    try:
        mycode = code.decode('utf-8')
    except:
        mycode = code
    return mycode

class IWebcodeMarker(Interface):
    pass

@provider(IFormFieldProvider)
class IWebcode(model.Schema):
    """
    """

    directives.fieldset(
            'webcode_dexterity',
            label=u'Webcode',
            fields=('webcode',),
        )

    webcode = schema.TextLine(
        title=u"Webcode",
        description=u"Eingabe des Webcodes für diesen Inhalt",
        defaultFactory=createWebcode,
        required=False,
        )


@implementer(IWebcode)
@adapter(IWebcodeMarker)
class Webcode(object):
    def __init__(self, context):
        self.context = context

    @property
    def webcode(self):
        if hasattr(self.context, 'webcode'):
            return self.context.webcode
        return None

    @webcode.setter
    def webcode(self, value):
        self.context.webcode = value
