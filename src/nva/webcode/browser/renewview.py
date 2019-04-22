# -*- coding: utf-8 -*-
from zope.interface import Interface
from DateTime import DateTime
import random
from plone import api as ploneapi
from Products.Five import BrowserView

class RenewWebcode(BrowserView):

    def webcodehandler(self, obj):
        """ Diese Methode wird immer dann aufgerufen wenn ein Dokument einen neuen Webcode erhalten soll.
            Mit der Methode soll eine 8-stellige, moeglichst eindeutige Zahl gebildet werden. Das
            soll durch folgende Methode erreicht werden:
            * Verkettung 2-stellige Jahreszahl(Konstante) + 6-stellige Zufallszahl
            * Catalogabfrage, ob im betr. Jahr ein Objekt mit dieser Kombination vorhanden ist, wenn ja:
            * wiederholter Aufruf des Zusfallszahlengenerators
        """
        if not hasattr(obj, 'webcode'):
            return
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
        #Setzen des Webcodes
        obj.webcode = unicode(code)
        return unicode(code)

    def __call__(self):
        self.code = self.webcodehandler(self.context)
        self.context.reindexObject()
        message = u"Für diesen Artikel wurde der folgende Webcode neu vergeben: %s" %self.code
        ploneapi.portal.show_message(message=message, request=self.request)
        return self.request.response.redirect(self.context.absolute_url())
