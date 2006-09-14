#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Author: David Vallejo Fernández ***********************#
#************************************************************#

import Ice, Glacier2
Ice.loadSlice('../MASYRO/MASYRO.ice', ['-I' '/usr/share/slice'])
import MASYRO
import sys

class TestI (MASYRO.Test):

    def hello (self, current):

        print 'It works!'
        try:
            obj = current.adapter.getCommunicator().stringToProxy('modelRepository')
            modelPrx = MASYRO.ModelRepositoryPrx.checkedCast(obj)
            modelPrx.hello()
        except:
            print 'Error en el cliente'
            sys.exit(0)

class Client (Ice.Application):

    def run (self, argv):

        self.shutdownOnInterrupt()

        # ConexiÃ³n con Glacier2.
        router = Glacier2.RouterPrx.checkedCast(self.communicator().getDefaultRouter())
        session = router.createSession('david', 'david')

        # Subscripción al Master.
        oa = self.communicator().createObjectAdapter('MyAdapter')
        ident = Ice.Identity()
        ident.name = Ice.generateUUID()
        ident.category = router.getServerProxy().ice_getIdentity().category
        prx = MASYRO.TestPrx.uncheckedCast(oa.add(TestI(), ident))

        obj = self.communicator().stringToProxy('master')
        masterPrx = MASYRO.MasterPrx.checkedCast(obj)
        masterPrx.subscribe('test', prx)

	self.communicator().waitForShutdown()
        
	return 0

Client().main(sys.argv, 'config/agent.cfg')
