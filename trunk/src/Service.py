#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern�ndez ************************#
#************************************************************#

import Ice
Ice.loadSlice('../FIPA/FIPA.ice', ['-I' '/usr/share/slice'])
import FIPA
import InputService

class Service:
    """La clase Service representa a un servicio genérico"""

    def __init__ (self):
        """Crea un objeto de tipo Service"""

        self.ServiceDirectoryEntry = FIPA.TServiceDirectoryEntry()
        self.Description = ''

    def init (self, inputFileXML):
        """Inicializa los parámetros ServiceDirectoryEntry y Description"""

        ins = InputService.InputService(inputFileXML)
        self.ServiceDirectoryEntry.ServiceType = ins.getServiceType()
        self.ServiceDirectoryEntry.ServiceId = ins.getServiceId()
        self.ServiceDirectoryEntry.ServiceLocator = ins.getServiceLocator()
        self.Description = ins.getDescription()

    def getServiceType (self):
        """Devuelve una cadena que representa el tipo del servicio"""
        return self.ServiceDirectoryEntry.ServiceType

    def getServiceId (self):
        """Devuelve una cadena que representa el id del servicio"""
        return self.ServiceDirectoryEntry.ServiceId

    def getServiceLocator (self):
        """Devuelve un objeto del tipo TServiceLocator"""
        return self.ServiceDirectoryEntry.ServiceLocator

    def getDescription (self):
        """Devuelve una cadena que representa la descripción del servicio"""
        return self.Description
