#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern�ndez ************************#
#************************************************************#

# VARIABLES QUE INDICAN EL VALOR MÁXIMO DE Recursion Level Y Lights per Sample
MAXRL, MAXLS = 9, 13

import Blender
from Blender import *
from Blender.Scene import Render
from Blender import Lamp, Object
import sys, math


def getFinalValue (current, new, max):
    """Devuelve el valor ponderado del valor obtenido por el sistema de reglas difuso"""

    f = math.fabs(float(new / max))
    f = getMax(0.5, f)
    final = int(f * current)
    
    if final <= 0:
        return 1
    else:
        return final

def getMax (v1, v2):
    """Devuelve el máximo de v1 y v2"""

    if v1 > v2:
        return v1
    else:
        return v2

def getFinalDimensions (x1, y1, x2, y2, ibs, resX, resY):
    """Devuelve las dimensiones finales del trozo, con la banda de interpolación"""

    if (x1 - ibs) >= 0:
        x1 -= ibs
    if (y1 - ibs) >= 0:
        y1 -= ibs
    if (x2 + ibs) <= resX:
        x2 += ibs
    if (y2 + ibs) <= resY:
        y2 += ibs

    return x1, y1, x2, y2

scn = Scene.GetCurrent()
context = scn.getRenderingContext()
context.setRenderPath('../src/' + sys.argv[7])
context.setImageType(Render.PNG)

(x1, y1, x2, y2) = [float(p) for p in sys.argv[8:12]]
(rl, ibs, ls) = [math.floor(float(p)) for p in sys.argv[12:15]]

currentRl = context.yafrayRayDepth()
finalRl = getFinalValue(currentRl, rl, MAXRL)

print 'Valor final de RecursionLevel: ' + str(finalRl)
print 'Valor final de InterpolationBandSize: ' + str(ibs)

lamps = Lamp.Get()
for l in lamps:
    l.setSamples(getFinalValue(l.getSamples(), ls, MAXLS))
    print 'Valor final de LightSamples: ' + str(l.getSamples())

# Actualización del nivel de recursión.
context.yafrayRayDepth(finalRl)

# Adaptación con los valores de interpolación.
print 'Trozo sin interpolación: [' + str(x1) + ', ' + str(y1) + ', ' + str(x2) + ', ' + str(y2) + ']'
x1, y1, x2, y2 = getFinalDimensions(x1, y1, x2, y2, ibs, context.imageSizeX(), context.imageSizeY())
print 'Trozo con interpolación: [' + str(x1) + ', ' + str(y1) + ', ' + str(x2) + ', ' + str(y2) + ']'

# Adaptación al método imageSizeXY.
aux = y1
y1 = context.imageSizeY() - y2
y2 = context.imageSizeY() - aux

x1 /= float(context.imageSizeX())
y1 /= float(context.imageSizeY())
x2 /= float(context.imageSizeX())
y2 /= float(context.imageSizeY())

context.enableBorderRender(1)
context.setBorder(x1, y1, x2, y2)
