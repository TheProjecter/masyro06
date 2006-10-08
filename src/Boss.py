#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Author: David Vallejo Fern�ndez ***********************#
#************************************************************#

import Ice, Glacier2
Ice.loadSlice('../MASYRO/MASYRO.ice', ['-I' '/usr/share/slice'])
import MASYRO
import Util, array, sys

DEFAULT_LEVEL = 3
DEFAULT_OPTIMIZATION_LEVEL = 3
DEFAULT_WORK_NAME = 'work'

class Boss (Ice.Application):
    """La clase Boss representa al elemento que envía trabajos al Analyst"""

    def getAnalystArguments (self, argv):
        """Devuelve los par�metros representativos a la hora de inicializar un analizador"""

        level, optimizationLevel, work, workName = DEFAULT_LEVEL, DEFAULT_OPTIMIZATION_LEVEL, '', DEFAULT_WORK_NAME

        for i in range(1, len(argv)):

            # -p ==> Nivel de división (1-3).
            if argv[i] == '-p':
                try:
                    level = int(argv[i + 1])
                except IndexError:
                    level = DEFAULT_LEVEL
                except ValueError:
                    level = DEFAULT_LEVEL

            # -o ==> Nivel de optimización (1-5).
            if argv[i] == '-o':
                try:
                    optimizationLevel = int(argv[i + 1])
                except IndexError:
                    optimizationLevel = DEFAULT_OPTIMIZATION_LEVEL
                except ValueError:
                    optimizationLevel = DEFAULT_OPTIMIZATION_LEVEL                    

            # -w ==> Fichero de trabajo (.zip).
            if argv[i] == '-w':
                try:
                    work = argv[i + 1]
                    l = work.split('.')
                    if l[1] != 'zip':
                        print 'El fichero de trabajo debe estar comprimido en formato zip.'
                        sys.exit(0)
                except:
                    print 'El fichero de trabajo especificado no es válido.'
                    sys.exit(0)

            # -n ==> Nombre del trabajo.
            if argv[i] == '-n':
                try:
                    workName = argv[i + 1]
                except:
                    print 'Usando ' + DEFAULT_WORK_NAME + ' como nombre del proyecto.'

        if work == '':
            print 'Debe especificar el fichero de trabajo.'
            print 'Sinopsis: python Boss.py -i <file.xml> [- p <level>] -w <path_to_workfile> [-n <work_name>]'
            sys.exit(0)

        return level, optimizationLevel, work, workName

    def run (self, argv):

        self.shutdownOnInterrupt()

        level, optimizationLevel, work, workName = self.getAnalystArguments(argv)
        #bytes = array.array('B', open(work).read()).tolist()

        # Conexión con Glacier2.
        router = Glacier2.RouterPrx.checkedCast(self.communicator().getDefaultRouter())
        session = router.createSession('david', 'david')

        # Envío del trabajo al analizador.
        obj = self.communicator().stringToProxy('analyst')
        prx = MASYRO.AnalystPrx.uncheckedCast(obj)
        prx.processWork(work, workName, level, optimizationLevel)

	self.communicator().waitForShutdown()
        
	return 0

Boss().main(sys.argv, 'config/agent.cfg')
