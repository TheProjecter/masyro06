#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern·ndez ************************#
#************************************************************#

import time, math

def getValue ():
    """Devuelve el tiempo en segundos empleado en la ejecuci√≥n del benchmark"""
    
    begin = time.time()
    benchmark()
    end = time.time()
    return end - begin

def benchmark ():

    a, b, c, = 0.0, 0.0, 0.0

    for i in range(1, 2000):
        for j in range(1, 2000):
            a = float(i / j)
            b = float(a * math.exp(3))
