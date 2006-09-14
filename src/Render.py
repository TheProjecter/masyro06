#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern�ndez ************************#
#************************************************************#

import Blender
from Blender import *
from Blender.Scene import Render

class Render:
    """La clase Render permite parametrizar el render"""

    def __init__ (self):
        """Crea un objeto del tipo Render"""

        self.RenderingContext = Scene.GetCurrent().getRenderingContext()

    def setRenderPath (self, renderPath):
        """Establece la ruta de salida del render"""
        self.getRenderingContext().setRenderPath(renderPath)

    def getRenderingContext (self):
        """Devuelve el contexto de renderizado actual"""
        return self.RenderingContext

    def setResX (self, resX):
        """Establece el valor del ancho de la imagen en píxeles"""
        self.getRenderingContext().imageSizeX(resX)

    def getResX (self):
        """Devuelve el valor del ancho de la imagen en píxeles"""
        return self.getRenderingContext().imageSizeX()

    def getResy (self):
        """Devuelve el valor de la altura de la imagen en píxeles"""
        return self.getRenderingContext().imageSizeY()

    def setResY (self, resY):
        """Establece el valor de la altura de la imagen en píxeles"""
        self.getRenderingContext().imageSizeY(resY)

    def setOversamplingLevel (self, level):
        """Establece el nivel de oversampling"""

        self.getRenderingContext().enableOversampling(1)
        self.getRenderingContext().setOversamplingLevel(level)

    def setRenderBorder (self, left, bottom, right, top):
        """Establece el trozo a renderizar"""

        self.getRenderingContext().enableBorderRender(1)
        self.getRenderingContext().setBorder(left, bottom, right, top)

    def setGeneralSettings (self):
        """Establece opciones generales"""

        self.getRenderingContext().setImageType(Render.PNG)
