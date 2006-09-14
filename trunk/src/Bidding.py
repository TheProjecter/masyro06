#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern�ndez ************************#
#************************************************************#

# Variable que representa la parte de histórico más reciente a tener en cuenta.
H = 3

class Bidding:
    """La clase Bidding representa una puja por parte de un agente"""

    def __init__ (self, agent, idWork, idZone, credits, historic, state):
        """Crea un objeto del tipo Bidding"""

        self.Agent = agent
        self.IdWork = idWork
        self.IdZone = idZone
        self.Credits = credits
        self.Historic = historic
        self.State = state

    def getAgent (self):
        """Devuelve el valor de la variable Agent"""
        return self.Agent

    def getIdWork (self):
        """Devuelve el valor de la variable IdWork"""
        return self.IdWork

    def getIdZone (self):
        """Devuelve el valor de la variable IdZone"""
        return self.IdZone

    def getCredits (self):
        """Devuelve el valor de la variable Credits"""
        return self.Credits

    def getHistoric (self):
        """Devuelve el valor de la variable Historic"""
        return self.Historic

    def getCurrentHistoric (self):
        """Devuelve el valor que representa el histórico más actual de la puja"""

        v = 0

        for j in range(len(self.getHistoric()) - len(self.getHistoric()) / H, len(self.getHistoric())):
            if self.getHistoric()[j] == 1:
                v += 1

        return v

    def setState (self, state):
        """Establece el valor de la variable State"""
        self.State = state

    def getState (self):
        """Devuelve el valor de la variable State"""
        return self.State

    def copy (self):
        """Devuelve una copia de la puja"""
        return Bidding(self.getAgent(), self.getIdWork(), self.getIdZone(), self.getCredits(), self.getHistoric(), self.getState())

    def __str__ (self):
        """Devuelve una cadena que representa a la puja"""

        return '[Agent: ' + self.getAgent() + ' IdWork: ' + str(self.getIdWork()) + ' IdZone: ' + str(self.getIdZone()) + ' Credits: ' + str(self.getCredits()) + ' HistoricValue: ' + str(self.getCurrentHistoric()) + ' State: ' + str(self.getState()) + ']'
