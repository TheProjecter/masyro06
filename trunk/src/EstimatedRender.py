#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern�ndez ************************#
#************************************************************#

import Blender
from Blender import *
from Blender.Scene import Render
import sys, os

scn = Scene.GetCurrent()
context = scn.getRenderingContext()
context.setRenderPath(sys.argv[7])

context.setImageType(Render.PNG)

(x1, y1, x2, y2) = [float(p) for p in sys.argv[8:12]]
RES = int(sys.argv[12])

# Adaptación al método imageSizeXY
aux = y1
y1 = context.imageSizeY() - y2
y2 = context.imageSizeY() - aux

x1 /= float(context.imageSizeX())
y1 /= float(context.imageSizeY())
x2 /= float(context.imageSizeX())
y2 /= float(context.imageSizeY())

context.enableBorderRender(1)
context.setBorder(x1, y1, x2, y2)

context.imageSizeX(context.imageSizeX() / RES)
context.imageSizeY(context.imageSizeY() / RES)
