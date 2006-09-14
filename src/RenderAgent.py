#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern·ndez ************************#
#************************************************************#

import sys, os, array, zipfile, time, math
import Ice, IceStorm
Ice.loadSlice('../FIPA/FIPA.ice', ['-I' '/usr/share/slice'])
import FIPA
Ice.loadSlice('../MASYRO/MASYRO.ice', ['-I' '/usr/share/slice'])
import MASYRO
import Agent
from Agent import *
import Zone
from Zone import *
import Util_fuzzy, Util, Benchmark
from Util_fuzzy import *

# Variable que representa el valor del tipo de servicio proporcionado.
TYPEOFSERVICE = 'render'
# Variable que especifica el % de disminuciÛn de la resoluciÛn.
RES = 10
# Variable que representa el n˙mero de crÈditos de partida del agente.
INITIAL_CREDITS = 10
# Variables que representan el valor de los premios y los fracasos.
PRIZE, FAILURE = 2, -1
GOODRESULT, BADRESULT = 1, 0
# Variable para el ajuste del coeficiente interno.
ADJUST = 0.1
# Variables que definen el n˙mero de particiones de los conjuntos difusos.
NUMPARTSCOMPLEXITY, NUMPARTSNEIGHBOUR, NUMPARTSSIZE, NUMPARTSOPTIMIZATION = 5, 5, 3, 5
# Variable que indica el archivo de carga del sistema difuso.
INPUTFUZZY = './init/fuzzyMasyro.xml'
INITDIR = './init/'
# Variables auxiliares.
INFINITO, MENOSINFINITO = 999999, -999999
# Peso asignado a Test para estimar la complejidad de una zona.
TEST_WEIGHT = 0.75
# Variable que indica la extensi√≥n de los ficheros.
EXT = '.png'

class AMI_Model_bidHigherI (object):

    def ice_response (self):
        print 'Puja terminada...'

    def ice_exception (self, ex):
        try:
            raise ex
        except Ice.LocalException:
            print 'Se produjo un error al pujar...'

class RenderAgentI (AgentI, MASYRO.RenderAgent):
    """La clase RenderAgentI representa a un agente especializado en el render"""

    def __init__ (self):
        """Crea un objeto del tipo RenderAgentI"""

        AgentI.__init__(self)
        # CurrentZones y CurrentIdWork representan al trabajo actual.
        self.CurrentZones, self.CurrentIdWork = [], -1
        # CurrentZone representa la zona de trabajo actual.
        self.CurrentIdZone = None
        # CurrentFiles representa los archivos asociados al trabajo actual.
        self.CurrentFiles = []
        # Credits representa los crÈditos de los que dispone un agente.
        self.Credits = INITIAL_CREDITS
        # Historic representa el histÛrico de Èxitos y fracasos de un agente.
        self.Historic = []
        # Coefficient representa el coeficiente interno del agente.
        self.Coefficient = 0
        # BenchmarkValue representa el tiempo medio de ejecuciÛn del benchmark en la plataforma MASYRO.
        self.BenchmarkValue = 0
        # State representa el estado del agente --> Estimating, Bidding, Rendering, Resting.
        self.State = MASYRO.StateRenderAgent.Resting

        # OptimizationLevel representa el nivel de optimizaci√≥n actual.
        self.OptimizationLevel = 0
        # FuzzySystem representa el sistema de reglas difuso.
        self.FuzzySystem = None

        # Master representa un proxy a un objeto del tipo Master.
        self.Master = None
        # Repository representa un proxy a un objeto del tipo ModelRepository.
        self.Repository = None
        # Proxy a la pizarra.
        self.Blackboard = None

        # Variable que representa el directorio de trabajo para un agente especializado en el render.
        self.WorkDir = self.getName()
        os.system('mkdir ' + self.getName())

    def obtainProxies (self):
        """Obtiene proxies a los servicios necesarios"""

        self.obtainMaster()
        self.obtainRepository()
        self.obtainBlackboard()

    def setCurrentZones (self, zones):
        """Establece el valor de CurrentZones"""
        self.CurrentZones = zones

    def getCurrentZones (self):
        """Devuelve el valor de CurrentZones"""
        return self.CurrentZones

    def getZone (self, zone):
        """Devuelve la zona con id zone"""

        for x in self.getCurrentZones():
            if x.id == zone:
                return x

    def setCurrentIdWork (self, idWork):
        """Establece el valor de CurrentIdWork"""
        self.CurrentIdWork = idWork

    def getCurrentIdWork (self):
        """Devuelve el valor de CurrentIdWork"""
        return self.CurrentIdWork

    def setCurrentIdZone (self, idZone):
        """Establece el valor de CurrentZone"""
        self.CurrentIdZone = idZone

    def getCurrentIdZone (self):
        """Devuelve el valor de CurrentZone"""
        return self.CurrentIdZone

    def setCurrentFiles (self, currentFiles):
        """Establece el valor de CurrentFiless"""
        self.CurrentFiles = currentFiles

    def getCurrentFiles (self):
        """Devuelve el valor de CurrentFiles"""
        return self.CurrentFiles

    def incrementCredits (self, value):
        """AÒade el valor value a la variable Credits"""
        self.Credits += value

    def getCredits (self):
        """Devuelve el valor de la variable Credits"""
        return self.Credits

    def addHistoric (self, value):
        """AÒade un nuevo valor al histÛrico"""
        self.Historic.append(value)

    def getHistoric (self):
        """Devuelve el valor de la variable Historic"""
        return self.Historic

    def setCoefficient (self, value):
        """Establece el valor de la variable Coefficient"""
        self.Coefficient = value

    def getCoefficient (self):
        """Devuelve el valor de la variable Coefficient"""
        return self.Coefficient

    def setBenchmarkValue (self, value):
        """Establece el valor de la variable BenchmarkValue"""
        self.BenchmarkValue = value

    def getBenchmarkValue (self):
        """Devuelve el valor de la variable BenchmarkValue"""
        return self.BenchmarkValue

    def setState (self, state):
        """Establece el valor de la variable State"""
        self.State = state

    def getState (self, current = None):
        """Devuelve el valor de la variable State"""
        return self.State

    def setOptimizationLevel (self, value):
        """Establece el valor de la variable OptimizationLevel"""
        self.OptimizationLevel = value

    def getOptimizationLevel (self):
        """Devuelve el valor de la variable OptimizationLevel"""
        return self.OptimizationLevel

    def setFuzzySystem (self, fuzzySystem):
        """Establece el valor de la variable FuzzySystem"""
        self.FuzzySystem = fuzzySystem

    def getFuzzySystem (self):
        """Devuelve el valor de la variable FuzzySystem"""
        return self.FuzzySystem

    def setMaster (self, master):
        """Establece un proxy a un agente del tipo Master"""
        self.Master = master

    def getMaster (self):
        """Devuelve un proxy a un agente del tipo Master"""
        return self.Master

    def obtainMaster (self):
        """Obtiene un proxy a un agente del tipo Master"""

        try:
            # B˙squeda de un master para enviarle el trabajo.
            self.setMaster(MASYRO.MasterPrx.checkedCast(self.communicator().stringToProxy('master')))
            return True

        except Ice.LocalException:
            print self.getName() + ' --> Fue incapaz de obtener un proxy a un Master.'
            return False

    def setRepository (self, repository):
        """Establece un proxy al servicio de repositorio"""
        self.Repository = repository

    def getRepository (self):
        """Devuelve un proxy al servicio de repositorio"""
        return self.Repository

    def obtainRepository (self):
        """Obtiene un proxy al repositorio de modelos"""

        try:
            obj = self.communicator().stringToProxy('modelRepository')
            self.setRepository(MASYRO.ModelRepositoryPrx.checkedCast(obj))
            
        except Ice.NotRegisteredException:
            proxy = self.communicator().getProperties().getProperty('IceGrid.InstanceName') + '/Query'
            query = IceGrid.QueryPrx.checkedCast(self.communicator().stringToProxy(proxy))
            self.setRepository(MASYRO.ModelRepositoryPrx.checkedCast(query.findObjectByType('::MASYRO::ModelRepository')))

        except Ice.LocalException:
            print self.getName() + ' --> No pudo obtener un proxy al repositorio de modelos.'

    def setBlackboard (self, blackboard):
        """Establece un proxy a la pizarra"""
        self.Blackboard = blackboard

    def getBlackboard (self):
        """Devuelve un proxy a la pizarra"""
        return self.Blackboard

    def obtainBlackboard (self):
        """Obtiene un proxy a la pizarra"""

        try:
            obj = self.communicator().stringToProxy('blackboard')
            self.setBlackboard(MASYRO.BlackboardPrx.checkedCast(obj))
            
        except Ice.NotRegisteredException:
            proxy = self.communicator().getProperties().getProperty('IceGrid.InstanceName') + '/Query'
            query = IceGrid.QueryPrx.checkedCast(self.communicator().stringToProxy(proxy))
            self.setBlackboard(MASYRO.BlackboardPrx.checkedCast(query.findObjectByType('::MASYRO::Blackboard')))

        except Ice.LocalException:
            print self.getName() + ' --> No pudo obtener un proxy a la pizarra.'                            
            
    def getWorkDir (self):
        """Devuelve el valor de la variable WorkDir"""
        return self.WorkDir

    def notifyNewWork (self, zones, idWork, benchmarkValue, current = None):
        """Obtiene la notificaciÛn de un nuevo evento asociado a un trabajo que notifica el Master al que est· subscrito"""

        print 'Nuevo trabajo disponible: ', idWork
        self.setCurrentZones(zones)
        self.setCurrentIdWork(idWork)
        self.setBenchmarkValue(benchmarkValue)
        self.work()

        print self.getName() + ' --> Cargando el sistema de reglas difuso...'
        self.loadFuzzySystem()

    def work (self):
        """Comienzo de un nuevo trabajo"""

        # Se obtiene el modelo de trabajo a partir del par·metro idWork.
        name, model = self.getRepository().get(self.getCurrentIdWork())
        
        # Se guarda el archivo recibido.
        path = os.path.join(self.getWorkDir(), name)
        array.array('B', model).tofile(open(path, 'w'))
        # Se extrae el contenido del archivo comprimido.
        unzip = Util.Unzip(path)
        # Se almacenan los nombres de los archivos contenidos en el archivo comprimido.
        nameList = unzip.extract(self.getWorkDir())
        self.setCurrentFiles(nameList)

    def notifyBenchmarkValue (self):
        """Notifica al Master el tiempo empleado en la ejecuciÛn del benchmark"""
        self.getMaster().benchmarkValue(int(Benchmark.getValue()))

    def notifyZones (self, zones, idWork, optimization, current = None):
        """Permite conocer las zonas a priori asignadas"""

        # Cambio de estado.
        self.setState(MASYRO.StateRenderAgent.Estimating)
        
        self.setOptimizationLevel(optimization)
        for z in zones:
            print self.getName() + ' --> Estimando... IdWork: ' + str(idWork) + ' WorkUnit: ' + str(z.id)
            self.estimatedRender(idWork, z.id)

        # Cambio de estado.
        self.setState(MASYRO.StateRenderAgent.Resting)

    def estimatedRender (self, idWork, idZone):
        """Realiza el render tamaÒo sello y escribe los datos obtenidos en la pizarra"""

        blenderFile = Util.getFileName(self.getCurrentFiles(), 'blend')
        ficheroBlender = os.path.join(self.getWorkDir(), blenderFile)
        
        salida = os.path.join(self.getWorkDir(), str(idWork) + '_' + str(idZone))
        zone = self.getZone(idZone)
        x1, y1 = zone.x1, zone.y1
        x2, y2 = zone.x2, zone.y2

        # Se toma la hora para actualizar el registro en la pizarra.
        begin = time.time()
        # Render con el script EstimatedRender.py.
        os.system('blender -b ' + ficheroBlender + ' -P ./EstimatedRender.py -f 1 ' + salida + ' ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' ' + str(RES))
        end = time.time()

        os.system('mv ' + salida + '0001.png ' + salida + EXT)

        # ActualizaciÛn en la pizarra con el tiempo estimado en el render tamaÒo "sello".
        self.getBlackboard().incrementEstimatedRenderTime(int(end - begin))
        
        if len(self.getHistoric()) == 0:
            self.setCoefficient(Benchmark.getValue() / self.getBenchmarkValue())
        finalTime = int(RES * (end - begin) / self.getCoefficient())
        self.getBlackboard().update(idWork, idZone, finalTime)

    def beginRenderProcess (self, current = None):
        """Notifica el comienzo del proceso de puja-render"""

        self.setState(MASYRO.StateRenderAgent.Bidding)

        # Lectura de los registros de la pizarra para pujar por una zona.
        idMostComplexZone, maxComplex = -1, -1
        for x in self.getCurrentZones():
            register = self.getBlackboard().read(self.getCurrentIdWork(), x.id)
            # Zona m√°s compleja ==> 75% peso Test 25% peso Comp.
            # Si la zona es m·s compleja que la actual y no ha sido cogida por ning˙n agente...
            maxTest = self.getBlackboard().getMaxTest(self.getCurrentIdWork())
            maxComp = self.getBlackboard().getMaxComp(self.getCurrentIdWork())
            currentZoneComplexity = self.getComplexityRatio(register.Test, maxTest, register.Comp, maxComp)
            if currentZoneComplexity > maxComplex and register.Agent == '':
                idMostComplexZone = x.id
                maxComplex = currentZoneComplexity

        # El agente puja por el trozo m·s complejo.
        if idMostComplexZone != -1:
            
            print self.getName() + ' --> Pujando por ' + str(self.getCurrentIdWork()) + ' ' + str(idMostComplexZone)
            cb = AMI_Model_bidHigherI()
            self.getMaster().bidHigher_async(cb, self.getName(), self.getCurrentIdWork(), idMostComplexZone, self.getCredits(), self.getHistoric())
        # En caso de que no pueda pujar, lo notifica al Master.
        else:
            # Cambio de estado.
            self.setState(MASYRO.StateRenderAgent.Finishing)
            self.getMaster().noMoreBiddings()

    def getComplexityRatio (self, test, maxTest, comp, maxComp):
        """Devuelve un valor ponderado que representa la complejidad del trozo"""

        return TEST_WEIGHT * (float(test * 100 / maxTest)) + (1 - TEST_WEIGHT) * (float(comp * 100 / maxComp))

    def render (self, idWork, idZone, agent, current = None):
        """Proceso de render de la zona idZone del trabajo idWork por parte del agente agent"""

        # Cambio de estado.
        self.setState(MASYRO.StateRenderAgent.Rendering)

        # Se actualiza la zona de trabajo actual.
        self.setCurrentIdZone(idZone)
        # Se lleva a cabo el render de la zona de trabajo actual.
        finalTime = self.finalRender(self.getOptimizationLevel())

        # Cambio de estado.
        self.setState(MASYRO.StateRenderAgent.Resting)

        # Proceso de ajuste de crÈditos, histÛrico, y coeficiente interno.
        self.internAdjustment(int(finalTime / self.getCoefficient()))
        
        # Puja por un nuevo trozo.
        self.beginRenderProcess()

    def finalRender (self, optimizationLevel):
        """Proceso de render final de la zona idZone"""

        blenderFile = Util.getFileName(self.getCurrentFiles(), 'blend')
        ficheroBlender = os.path.join(self.getWorkDir(), blenderFile)
        salida = os.path.join(self.getWorkDir(), str(self.getCurrentIdWork()) + '_' + str(self.getCurrentIdZone()))

        # Se obtiene la zona identificada por idZone.
        zone = self.getZone(self.getCurrentIdZone())
        x1, y1 = zone.x1, zone.y1
        x2, y2 = zone.x2, zone.y2
        aux = ' Zone: [' + str(x1) + ', ' + str(y1) + ', ' + str(x2) + ', ' + str(y2) + ']'
        print 'Rendering... ' + str(self.getCurrentIdWork()) + ' ' + str(self.getCurrentIdZone()) + aux

        # Se obtienen los par·metros de salida del sistema difuso.
        data = self.loadDataFuzzySystem(optimizationLevel)
        rl, ibs, ls = -1, -1, -1
        for x in data.keys():
            if x == 'Rl':
                rl = data[x]
            elif x == 'Ibs':
                ibs = data[x]
            elif x == 'Ls':
                ls = data[x]

        # Se toma la hora para actualizar el registro en la pizarra.
        begin = time.time()
        os.system('blender -b ' + ficheroBlender + ' -P ./FinalRender.py -f 1 ' + salida + ' ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' ' + str(rl) + ' ' + str(ibs) + ' ' + str(ls))
        end = time.time()

        # ActualizaciÛn en la pizarra.
        finalTime = int((end - begin))
        self.getBlackboard().finishWorkUnit(self.getCurrentIdWork(), self.getCurrentIdZone(), finalTime, int(ibs), int(ls), int(rl))

        os.system('mv ' + salida + '0001.png ' + salida + EXT)

        # Env√≠o al Master de la zona renderizada.
        salida += EXT
        partialImage = array.array('B', open(salida).read()).tolist()
        self.getMaster().giveFinalImage(self.getCurrentIdWork(), self.getCurrentIdZone(), partialImage, x1, y1,x2, y2, int(ibs))

        return finalTime

    def loadDataFuzzySystem (self, optimizationLevel):
        """Carga los datos de entrada del sistema de reglas difuso"""

        c = self.getCurrentFuzzyComplexity()
        nd = self.getCurrentFuzzyNeighbourDifference()
        s = self.getCurrentFuzzySize()

        print 'C: ' + str(c) + ' Nd: ' + str(nd) + ' S: ' + str(s) + ' Op: ' + str(optimizationLevel)

        # Datos de entrada para el sistema de reglas difuso.
        inputData = []
        inputData.append((('C', c), ('Nd', nd), ('S', s), ('Op', optimizationLevel * 5)))

        for x in inputData:
            a, b, c = self.getFuzzySystem().evalAll(x)
            return self.getFuzzySystem().out(x)

    def loadFuzzySystem (self):
        """Carga la informaciÛn necesaria en el sistema de reglas difuso"""

        # ObtenciÛn par·metros de entrada del sistema difuso --> Complejidad, diferencia entre vecinos, tamaÒo, y nivel de optimizaciÛn.
        complexity = self.getFuzzyComplexity()
        neighbourDifference = self.getFuzzyNeighbourDifference()
        size = self.getFuzzySize()

        fuzzy = UtilFuzzy()
        xmlFile = os.path.join(INITDIR, self.getName() + '.xml')
        os.system('cp ' + INPUTFUZZY + ' ' + xmlFile)
        
        # ActualizaciÛn del archivo que especifica el sistema difuso.
        Util.createInput(self.getName() + '.txt', complexity, neighbourDifference, size)
        sInput, cInput, ndInput = Util.loadInput(self.getName() + '.txt')

        # Carga del sistema de reglas difuso en memoria.
        fuzzy.loadInputData(sInput, cInput, ndInput, xmlFile)
        fuzzy.loadFile(xmlFile)

        self.setFuzzySystem(FuzzySystem(fuzzy.getSystemName()))
        
        # Variables del sistema.
        for x in fuzzy.getVariables():
            self.getFuzzySystem().insertVar(x)

        # Reglas del sistema.
        for i in range(len(fuzzy.getAntecedents())):
            self.getFuzzySystem().insertRule(fuzzy.getAntecedents()[i], fuzzy.getConsequences()[i])

    def internAdjustment (self, finalTime):
        """Proceso de ajuste de crÈditos, histÛrico, y coeficiente interno"""

        # Obtenemos la informaciÛn de la zona idZone.
        register = self.getBlackboard().read(self.getCurrentIdWork(), self.getCurrentIdZone())
        # Obtenemos el tiempo que previamente se estimÛ.
        test = register.Test
        # El render tendr· premio si se realizÛ con un determinado margen de error.
        testRange = (int(test - test / RES), int(test + test / RES))
        if finalTime <= testRange[1]:
            # Premio --> Incrementar crÈditos y actualizar histÛrico.
            print '°PREMIO! --> IdWork: ' + str(self.getCurrentIdWork()) + ' IdZone: ' + str(self.getCurrentIdZone()) + ' Test: ' +str(test) + ' Treal: ' + str(finalTime)
            self.incrementCredits(PRIZE)
            self.getHistoric().append(GOODRESULT)
            # Aunque se hizo el render a tiempo, es preciso ajustar el coeficiente interno.
            if finalTime <= testRange[0]:
                self.adjustInternCoefficient(True, finalTime, testRange[0])

        else:
            # PenalizaciÛn --> Decrementar crÈditos y actualizar histÛrico.
            print '°FRACASO! --> IdWork: ' + str(self.getCurrentIdWork()) + ' IdZone: ' + str(self.getCurrentIdZone()) + ' Test: ' +str(test) + ' Treal: ' + str(finalTime)
            self.incrementCredits(FAILURE)
            self.getHistoric().append(BADRESULT)
            # Ajuste del coeficiente interno.
            self.adjustInternCoefficient(False, finalTime, testRange[1])

    def adjustInternCoefficient (self, increment, finalTime, test):
        """Ajusta el coeficiente interno en funciÛn de increment (True --> incrementa, False --> decrementa)"""

        print '***Coeficiente actual: ' + str(self.getCoefficient())
        if increment:
            self.setCoefficient(self.getCoefficient() + (self.getCoefficient() * ADJUST))
        else:
            self.setCoefficient(self.getCoefficient() - (self.getCoefficient() * ADJUST))
        print '***Coeficiente cambiado: ' + str(self.getCoefficient())

    def getFuzzyComplexity (self):
        """Devuelve la complejidad de la zona y las particiones asociadas a la complejidad """

        complexity = {}
        minComp, maxComp = INFINITO, MENOSINFINITO

        for zone in self.getCurrentZones():
            if zone.m < minComp:
                minComp = zone.m
            if zone.m > maxComp:
                maxComp = zone.m

        interval = (maxComp - minComp) / (NUMPARTSCOMPLEXITY + 1)
        minComp -= 1
        maxComp += 1

        complexity['VS'] = (minComp, minComp, minComp + interval, minComp + 2 * interval)
        complexity['S'] = (minComp + interval, minComp + 2 * interval, minComp + 2 * interval, minComp + 3 * interval)
        complexity['N'] = (minComp + 2 * interval, minComp + 3 * interval, maxComp - 3 * interval, maxComp - 2 * interval)
        complexity['B'] = (maxComp - 3 * interval, maxComp - 2 * interval, maxComp - 2 * interval, maxComp - interval)
        complexity['VB'] = (maxComp - 2 * interval, maxComp - interval, maxComp, maxComp)

        return complexity

    def getCurrentFuzzyComplexity (self):
        """Devuelve la complejidad de la zona de trabajo actual"""
        return self.getBlackboard().read(self.getCurrentIdWork(), self.getCurrentIdZone()).Comp

    def getFuzzyNeighbourDifference (self):
        """Devuelve la diferencia de vecindad de la zona idZone con el resto"""

        zone = self.getZone(self.getCurrentIdZone())
        differences = {}
        aux = []

        # Estudio de la diferencia de complejidad entre todos los vecinos.
        for x in self.getCurrentZones():
            ac = 0
            for y in self.getCurrentZones():
                if x.id != y.id and self.isNeighbour(x, y):
                    ac += self.getNeighbourDifference(x, y)
            aux.append(ac)

        aux.sort()
        minD, maxD = aux[0], aux[len(aux) - 1]
        interval = (maxD - minD) / (NUMPARTSNEIGHBOUR + 1)
        minD -= 1
        maxD += 1

        differences['VS'] = (minD, minD, minD + interval, minD + 2 * interval)
        differences['S'] = (minD + interval, minD + 2 * interval, minD + 2 * interval, minD + 3 * interval)
        differences['N'] = (minD + 2 * interval, minD + 3 * interval, maxD - 3 * interval, maxD - 2 * interval)
        differences['B'] = (maxD - 3 * interval, maxD - 2 * interval, maxD - 2 * interval, maxD - interval)
        differences['VB'] = (maxD - 2 * interval, maxD - interval, maxD, maxD)

        return differences

    def getCurrentFuzzyNeighbourDifference (self):
        """Devuelve la diferencia de vecindad de la zona actual de trabajo con respecto a sus zonas vecinas"""

        # Estudio de la diferencia de complejidad entre todos los vecinos.
        for x in self.getCurrentZones():
            ac = 0
            for y in self.getCurrentZones():
                if x.id != y.id and self.isNeighbour(x, y):
                    ac += self.getNeighbourDifference(x, y)
            # Diferencia de complejidad de vecinos del trozo actual.
            if x.id == self.getCurrentIdZone():
                return ac

    def isNeighbour (self, zone1, zone2):
        """Comprueba si las zonas zone1 y zone2 son vecinas"""

        if (zone1.x2 == zone2.x1 and zone1.y1 == zone2.y1) or (zone1.y2 == zone2.y1 and zone1.x1 == zone2.x1) or (zone2.x2 == zone1.x1 and zone2.y1 == zone1.y1) or (zone1.x1 == zone2.x1 and zone2.y2 == zone1.y1):
            return True
        else:
            return False

    def getNeighbourDifference (self, zone1, zone2):
        """Devuelve la diferencia de complejidad entre dos zonas vecinas"""
        return math.fabs(zone1.m - zone2.m)

    def getFuzzySize (self):
        """Devuelve el tamaÒo de la zona y las particiones asociadas al tamaÒo del trozo"""

        size = {}
        minComp, maxComp = INFINITO, MENOSINFINITO

        for zone in self.getCurrentZones():
            s = Util.getZoneSize(zone.x1, zone.y1, zone.x2, zone.y2)
            if s < minComp:
                minComp = s
            if s > maxComp:
                maxComp = s

        interval = (maxComp - minComp) / (NUMPARTSSIZE + 1)
        minComp -= 1
        maxComp += 1

        size['S'] = (minComp, minComp, minComp + interval, minComp + 2 * interval)
        size['N'] = (minComp + interval, minComp + 2 * interval, maxComp - 2 * interval, maxComp - interval)
        size['B'] = (maxComp - 2 * interval, maxComp - interval, maxComp, maxComp)

        return size

    def getCurrentFuzzySize (self):
        """Devuelve el tamaÒo de la zona actual de trabajo"""

        reg = self.getBlackboard().read(self.getCurrentIdWork(), self.getCurrentIdZone())
        z = self.getZone(self.getCurrentIdZone())
        s = Util.getZoneSize(z.x1, z.y1, z.x2, z.y2)

        return s

    def addRenderService (self, serviceName, serviceType):
        """AÒade el servicio identificado por serviceName a su lista de servicios"""
        self.addService(serviceName, serviceType)

    def subscribeMaster (self, prx):
        """Habilita la subscripciÛn a un servicio del tipo Master"""

        self.getMaster().subscribe(self.getName(), prx)
        print self.getName() + ' --> Registrado en el master.'

    def unsubscribeMaster (self):
        """Habilita la eliminaciÛn de la subscripciÛn a un servicio del tipo Master"""

        self.getMaster().unsubscribe(self.getName())
        print self.getName() + ' --> Dado de baja en el master.'

    def clear (self):
        """Libera recursos y elimina ficheros usados"""

        xmlFile = os.path.join(INITDIR, self.getName() + '.xml')
        os.system('rm -f ' + xmlFile)
        os.system('rm -f ' + self.getName() + '.txt')
        os.system('rm -rf ' + self.getName())

    def run (self, argv):
        """EjecuciÛn del cÛdigo asociado al renderAgent"""
                
        self.shutdownOnInterrupt()

        # Conexi√≥n con Glacier2.
        router = Glacier2.RouterPrx.checkedCast(self.communicator().getDefaultRouter())
        session = router.createSession('david', 'david')
        
        self.obtainServiceRoot()
        self.getBasicServices()
        self.addRenderService('render', TYPEOFSERVICE)

        # SubscripciÛn al DirectoryFacilitator.
        self.subscribeDF()

        ### ACCIONES ESPEC√çFICAS.
        self.obtainProxies()
        # Informar del tiempo de ejecuciÛn del benchmark.
        self.notifyBenchmarkValue()
        ### FIN ACCIONES ESPEC√çFICAS.

        # SubscripciÛn al Master.
        oa = self.communicator().createObjectAdapter('MyAdapter')
        ident = Ice.Identity()
        ident.name = Ice.generateUUID()
        ident.category = router.getServerProxy().ice_getIdentity().category
        prx = MASYRO.RenderAgentPrx.uncheckedCast(oa.add(self, ident))
        self.subscribeMaster(prx)

	self.communicator().waitForShutdown()
        # Baja del DirectoryFacilitator y del AMS.
        self.deregister()
        self.unsubscribeDF()
        # EliminaciÛn de la subscripciÛn al Master.
        self.unsubscribeMaster()
        # Limpieza de recursos.
        self.clear()

	return 0

RenderAgentI().main(sys.argv, 'config/agent.cfg')

