#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fernández ************************#
#************************************************************#

l = {}

l[(1, 1)] = 'a'
l[(1, 2)] = 'a'
l[(1, 3)] = 'a'
l[(1, 4)] = 'a'
l[(2, 1)] = 'a'
l[(2, 2)] = 'a'

r = 0

for x in l.keys():
    print x
    if x[0] == 2:
        r += 1

print r
