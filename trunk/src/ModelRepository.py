#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern�ndez ************************#
#************************************************************#

import sys, os, array, Ice, IceGrid
Ice.loadSlice('../FIPA/FIPA.ice', ['-I' '/usr/share/slice'])
import FIPA
Ice.loadSlice('../MASYRO/MASYRO.ice', ['-I' '/usr/share/slice'])
import MASYRO
import Util
import Service
from Service import *

# Variable que representa el directorio de trabajo para el servicio de repositorio de modelos.
MODEL_WORK_DIR = './models'
# Extensión de los ficheros comprimidos.
EXT = '.zip'

class ModelRepositoryI (MASYRO.ModelRepository, Ice.Application, Service):
    """La clase ModelRepositoryI representa un repositorio de modelos"""

    def __init__ (self):
        """Crea un objeto de tipo ModelRepositoryI"""

        Service.__init__(self)
        self.Models = {}
        self.NumberOfModels = 0

    def incrementNumberOfModels (self):
        """Incremente el n�mero de modelos en una unidad"""
        self.NumberOfModels += 1

    def decrementNumberOfModels (self):
        """Decrementa el n�mero de modelos en una unidad"""
        self.NumberOfModels -= 1

    def getNumberOfModels (self):
        """Devuelve el n�mero de modelos"""
        return self.NumberOfModels

    def addModel (self, name):
        """A�ade el modelo cuyo nombre es name y contenido model al conjunto de modelos"""

        self.incrementNumberOfModels()
        self.Models[self.getNumberOfModels()] = name

    def getModels (self):
        """Devuelve el diccionario de modelos"""
        return self.Models

    def getModelName (self, idModel):
        """Devuelve el nombre del modelo correspondiente al identificador idModel"""

        if self.getModels().has_key(idModel):
            return self.Models[idModel]
        else:
            raise KeyError

    def put (self, name, model, current = None):
        """A�ade el modelo cuyo nombre es name y contenido model al conjunto de modelos"""

        print 'ModelRepository --> Almacenando ' + name
        # Se guarda el modelo recibido en memoria f�sica.
        path = os.path.join(MODEL_WORK_DIR, name)
        array.array('B', model).tofile(open(path + EXT, 'w'))

        # Se almacena el modelo en el conjunto de modelos.
        self.addModel(name)

        # Devuelve el identificador asignado al modelo, que se corresponde con el n�mero de modelos existentes.
        return self.getNumberOfModels()

    def get (self, idModel, current = None):
        """Devuelve el nombre del modelo y la secuencia de bytes que lo representa"""

        print self.getServiceId() + ' --> Accediendo al repositorio de modelos...'
        try:
            name = self.getModelName(idModel)
        except KeyError:
            raise MASYRO.ModelNotExistsException('El modelo especificado no existe', self.getModels().keys())

        path = os.path.join(MODEL_WORK_DIR, name + EXT)
        model = array.array('B', open(path).read()).tolist()

        return name, model

    def registerAsWKO (self):
        """Registra a ModelRepository como un objeto bien conocido"""

        properties = self.communicator().getProperties()
        adapter = self.communicator().createObjectAdapter('ModelRepositoryAdapter')
        id = Ice.stringToIdentity(properties.getProperty('IdentityMR'))

        self.init(properties.getProperty('InputMR'))

        adapter.add(self, id)
        adapter.activate()

    def run (self, args):
        """Ejecuci�n del c�digo asociado al ModelRepository"""
                
        self.shutdownOnInterrupt()

        self.registerAsWKO()
        
	self.communicator().waitForShutdown()
	return 0

ModelRepositoryI().main(sys.argv, 'config/localServices.cfg')
