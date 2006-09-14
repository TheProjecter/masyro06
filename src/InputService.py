#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern�ndez ************************#
#************************************************************#

import xml.dom.minidom
from xml.dom.minidom import parse, parseString
import Ice
Ice.loadSlice('../FIPA/FIPA.ice', ['-I' '/usr/share/slice'])
import FIPA
import UtilXML

class InputService:
    """La clase InputService representa la funcionalidad asociada a la inicialización de un servicio"""

    def __init__ (self, file):
        """Crea un objeto del tipo InputService"""

        self.ServiceLocator = []
        
        doc = parse(file)
        root = doc.firstChild

        # Se obtiene el nombre del servicio.
        self.ServiceName = UtilXML.getAttribute(root, 'name')

        # Se obtiene la descripción del servicio y sus parámetros.
        for x in root.childNodes:
            if x.nodeType == x.ELEMENT_NODE and x.nodeName == 'serviceDirectoryEntry':
                self.ServiceType = UtilXML.getAttribute(x, 'serviceType')
                self.ServiceId = UtilXML.getAttribute(x, 'serviceId')
                # Se obtienen los Service Locators.
                for y in x.childNodes:
                    if y.nodeType == y.ELEMENT_NODE and y.nodeName == 'serviceLocator':
                        sld = FIPA.TServiceLocationDescription(UtilXML.getAttribute(y, 'serviceSignature'), UtilXML.getAttribute(y, 'serviceAddress'))
                        self.ServiceLocator.append(sld)
            elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'description':
                self.Description = x.firstChild.nodeValue

    def getServiceName (self):
        """Devuelve una cadena que representa el nombre del servicio"""
        return self.ServiceName

    def getServiceType (self):
        """Devuelve una cadena que representa el tipo del servicio"""
        return self.ServiceType

    def getServiceId (self):
        """Devuelve una cadena que representa el id del servicio"""
        return self.ServiceId

    def getServiceLocator (self):
        """Devuelve un objeto del tipo TServiceLocator"""
        return self.ServiceLocator

    def getDescription (self):
        """Devuelve una cadena que representa la descripción del servicio"""
        return self.Description
