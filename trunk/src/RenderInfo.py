#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern·ndez ************************#
#************************************************************#

class RenderInfo:
    """Clase que representa la informaci√≥n del render asociado a una puja"""

    def __init__ (self, idWork, idZone, agent):
        """Crea un objeto del tipo RenderInfo"""

        self.IdWork = idWork
        self.IdZone = idZone
        self.Agent = agent

    def getIdWork (self):
        """Devuelve el valor de la variable IdWork"""
        return self.IdWork

    def getIdZone (self):
        """Devuelve el valor de la variable IdZone"""
        return self.IdZone

    def getAgent (self):
        """Devuelve el valor de la variable Agent"""
        return self.Agent    
