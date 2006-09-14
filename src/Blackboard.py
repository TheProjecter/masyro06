#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern�ndez ************************#
#************************************************************#

import sys, os, array
import Ice, IceGrid
Ice.loadSlice('../FIPA/FIPA.ice', ['-I' '/usr/share/slice'])
import FIPA
Ice.loadSlice('../MASYRO/MASYRO.ice', ['-I' '/usr/share/slice'])
import MASYRO
import Util
import Service
from Service import *

class BlackboardI (MASYRO.Blackboard, Ice.Application, Service):
    """La clase BlackboardI representa la arquitectura de pizarra"""

    def __init__ (self):
        """Crea un objeto de tipo BlackboardI"""

        Service.__init__(self)
        # (Clave, Valor) == ((IdWork, IdZone), Register)
        self.Registers = {}
        # AnalysisTime representa el tiempo en segundos dedicado al análisis de la escena más reciente.
        self.AnalysisTime = 0
        # EstimatedRenderTime representa el tiempo en segundos dedicado a la estimación de las unidades de trabajo.
        self.EstimatedRenderTime = 0

    def addRegister (self, register):
        """Añade un registro a la lista de Registros"""
        self.Registers[(register.IdWork, register.WorkUnit)] = register

    def getRegisters (self):
        """Devuelve el diccionario de registros"""
        return self.Registers

    def write (self, register, current = None):
        """Escribe el registro register en la pizarra"""
        self.addRegister(register)

    def read (self, idWork, workUnit, current = None):
        """Lee el registro identificado por idWork, workUnit de la pizarra"""

        if self.getRegisters().has_key((idWork, workUnit)):
            return self.getRegisters()[(idWork, workUnit)]
        else:
            raise MASYRO.RegisterNotExistsException('El registro ' + str(idWork) + ', ' + str(workUnit) + ' no existe.')

    def update (self, idWork, workUnit, test, current = None):
        """Actualiza el registro register de la pizarra"""
        
        if self.getRegisters().has_key((idWork, workUnit)):
            self.getRegisters()[(idWork, workUnit)].Test = test
        else:
            raise MASYRO.RegisterNotExistsException('El registro ' + str(idWork) + ', ' + str(workUnit) + ' no existe.')

    def setAnalysisTime (self, time, current = None):
        """Establece el valor de la variable AnalysisTime"""
        self.AnalysisTime = time

    def getAnalysisTime (self, current = None):
        """Devuelve el valor de la variable AnalysisTime"""
        return self.AnalysisTime

    def setEstimatedRenderTime (self, time):
        """Establece el valor de la variable EstimatedRenderTime"""
        self.EstimatedRenderTime = time

    def incrementEstimatedRenderTime (self, time, current = None):
        """Devuelve el valor de la variable EstimatedRenderTime"""
        self.EstimatedRenderTime += time

    def getEstimatedRenderTime (self, current = None):
        """Incrementa el valor de la variable EstimatedRenderTime"""
        return self.EstimatedRenderTime

    def clear (self, current = None):
        """Limpia el contenido de la pizarra"""
        self.getRegisters().clear()
        self.setEstimatedRenderTime(0)

    def isWorkPartiallyEstimated (self, current = None):
        """Indica si todas las zonas del trabajo actual han sido estimadas"""

        estimatedZones = 0

        for r in self.getRegisters().values():
            if r.Test <> 0:
                estimatedZones += 1

        if estimatedZones == len(self.getRegisters()):
            return True
        else:
            return False

    def isCurrentWorkFinished (self, current = None):
        """Indica si el trabajo actual ha terminado"""

        for r in self.getRegisters().values():
            if r.State != MASYRO.StateRegister.Done:
                return False

        return True

    def show (self, current = None):
        """Muestra el contenido de la pizarra"""
        return self.__str__()

    def getMaxTest (self, idWork, current = None):
        """Devuelve el valor del trozo cuyo tiempo estimado es el mayor del trabajo idWork"""

        maxTest = -1

        for x in self.getRegisters().values():
            if x.IdWork == idWork and x.Test > maxTest:
                maxTest = x.Test

        return maxTest

    def getMaxComp (self, idWork, current = None):
        """Devuelve el valor del trozo cuya complejidad es la mayor del trabajo idWork"""

        maxComp = -1

        for x in self.getRegisters().values():
            if x.IdWork == idWork and x.Comp > maxComp:
                maxComp = x.Comp

        return maxComp

    def setWorkUnit (self, idWork, workUnit, agent, current = None):
        """Permite a un agente hacerse cargo de una unidad de trabajo"""

        if self.getRegisters().has_key((idWork, workUnit)):
            self.getRegisters()[(idWork, workUnit)].Agent = agent
            self.getRegisters()[(idWork, workUnit)].State = MASYRO.StateRegister.InWork
        else:
            raise MASYRO.RegisterNotExistsException('El registro ' + str(idWork) + ', ' + str(workUnit) + ' no existe.')

    def finishWorkUnit (self, idWork, workUnit, treal, ibs, ls, rl, current = None):
        """Permite a un agente notificar la finalización de una unidad de trabajo"""

        if self.getRegisters().has_key((idWork, workUnit)):
            self.getRegisters()[(idWork, workUnit)].Treal = int(treal)
            self.getRegisters()[(idWork, workUnit)].State = MASYRO.StateRegister.Done
            self.getRegisters()[(idWork, workUnit)].Ibs = ibs
            self.getRegisters()[(idWork, workUnit)].Ls = ls
            self.getRegisters()[(idWork, workUnit)].Rl = rl
        else:
            raise MASYRO.RegisterNotExistsException('El registro ' + str(idWork) + ', ' + str(workUnit) + ' no existe.')

    def getTimeCurrentWorks (self, current = None):
        """Devuelve el tiempo empleado en los trabajos escritos en la pizarra"""

        agents = {}

        for x in self.getRegisters().values():
            if not x.Agent in agents.keys():
                agents[x.Agent] = x.Treal
            else:
                agents[x.Agent] += x.Treal

        seconds = max(agents.values())
        tTotal = '[H: ' + str(seconds / 3600) + ' M: ' + str(seconds % 3600 / 60) + ' S: ' + str(seconds % 3600 % 60) + ']\n'

        straux = 'Tiempo empleado: ' + tTotal
        
        for x in agents.items():
            straux += (x[0] + '-->[H: ' + str(x[1] / 3600) + ' M: ' + str(x[1] % 3600 / 60) + ' S: ' + str(x[1] % 3600 % 60) + ']\n')

        return straux

    def __str__ (self):
        """Devuelve una cadena que representa a la pizarra"""

        straux = 'Blackboard: ' + '\n'

        for x in self.getRegisters().values():
            straux = straux + 'IdWork: ' + str(x.IdWork) + ' WorkUnit: ' + str(x.WorkUnit) + ' Size: ' + str(x.Size) + ' Comp: ' + str(x.Comp) + ' Test: ' + str(x.Test) + ' Treal: ' + str(x.Treal) + ' Agent: ' + str(x.Agent) + ' State: ' + x.State.__str__() + ' Ibs: ' + str(x.Ibs) + ' Ls: ' + str(x.Ls) + ' Rl: ' + str(x.Rl) + '\n'

        return straux

    def registerAsWKO (self):
        """Registra a Blackboard como un objeto bien conocido"""

        properties = self.communicator().getProperties()
        adapter = self.communicator().createObjectAdapter('BlackboardAdapter')
        id = Ice.stringToIdentity(properties.getProperty('IdentityBB'))

        self.init(properties.getProperty('InputBB'))

        adapter.add(self, id)
        adapter.activate()

    def run (self, args):
        """Ejecuci�n del c�digo asociado a la pizarra"""
                
        self.shutdownOnInterrupt()

        self.registerAsWKO()
        
	self.communicator().waitForShutdown()
	return 0

BlackboardI().main(sys.argv, 'config/localServices.cfg')
