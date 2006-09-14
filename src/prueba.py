#!/usr/bin/python
# -*- coding: utf-8 -*-

l = [1,2,3,4,5,6,7,8,9,10,11, 12]

numberOfAgents = 3
zonesPerBlock = max(int(len(l) / numberOfAgents), 1)

for a in range(numberOfAgents):
    if a <> numberOfAgents - 1:
        zones = l[a*zonesPerBlock:(a+1)*zonesPerBlock]
    else:
        zones = l[a*zonesPerBlock:len(l)]
    print zones
