#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern�ndez ************************#
#************************************************************#

import sys, os, array, zipfile, time
import Image
import Ice, Glacier2, IceGrid
Ice.loadSlice('../FIPA/FIPA.ice', ['-I' '/usr/share/slice'])
import FIPA
Ice.loadSlice('../MASYRO/MASYRO.ice', ['-I' '/usr/share/slice'])
import MASYRO
import Agent, Bidding, RenderInfo, Util, Util_image
from Agent import *
from Bidding import *
from RenderInfo import *
import Service
from Service import *

# Variable que representa el directorio de trabajo para un agente especializado en la gestión de un trabajo.
MASTER_WORK_DIR = './master'
MASYRO_WEB_DIR = "/var/www/masyro"
# Variables utilizadas para la asignación de pujas.
ASIGNED = 1
NOASIGNED = 0
WITHOUTPOSSIBILITY = -1
# Variable que indica la extensión de los ficheros.
EXT = '.png'
# Variable que indica el nombre del fichero de salida final.
SALIDA = 'salida.png'
# Variable que indica el nombre del fichero de log.
LOG = MASTER_WORK_DIR + '/log.txt'

class AMI_Model_renderI (object):
    """La clase AMI_Model_renderI representa la clase cuyos objetos recibirán los resultados de las llamadas asíncronas"""

    def ice_response (self):
        """Notifica la finalización del evento"""
        print 'Render terminado...'

    def ice_exception (self, ex):
        """Maneja las posibles excepciones de las invocaciones asíncronas"""
        
        try:
            raise ex
        except Ice.LocalException:
            print 'Se produjo un error al realizar el render...'

class AMI_Model_notifyZonesI (object):
    """La clase AMI_Model_notifyZoneI representa la clase cuyos objetos recibirán los resultados de las llamadas asíncronas"""

    def ice_response (self):
        """Notifica la finalización del evento"""
        print 'Notificacion realizada...'

    def ice_exception (self, ex):
        """Maneja las posibles excepciones de las invocaciones asíncronas"""
        
        try:
            raise ex
        except Ice.LocalException:
            print 'Se produjo un error al realizar la notificacion...'

class MasterI (MASYRO.Master, Ice.Application, Service):
    """La clase MasterI representa un gestor especializado en la gestión del trabajo asociado a un modelo"""

    def __init__ (self):
        """Crea un objeto del tipo MasterI"""

        Service.__init__(self)
        # CurrentZones y CurrentIdWork representan al trabajo actual.
        self.CurrentZones, self.CurrentIdWork = [], -1
        # CurrentImage representa la imagen final relativa al trabajo actual.
        self.CurrentImage = None
        # RenderAgents representa a los agentes especializados en el render.
        # (Clave, Valor) == (Nombre del agente, Proxy al agente)
        self.RenderAgents = {}
        # BenchmarkValue representa el tiempo medio de ejecución del benchmark en la plataforma MASYRO.
        self.BenchmarkValue = 1
        # Biddings representa las pujas actuales de los agentes.
        self.Biddings = []
        self.InitialBidding = 1
        # NumberOfPieces representa el número de trozos del trabajo actual que han llegado.
        self.NumberOfPieces = 0
        # CurrentBiddingTime representa el tiempo empleado para las distintas pujas.
        self.CurrentBiddingTime = 0

        # Proxies a distintos servicios.
        self.Repository, self.Blackboard = None, None

        # Log del Master.
        self.Log = ""
        # Tiempos finales asociados al trabajo.
        self.FinalTimes = ""

    def obtainProxies (self):
        """Obtiene proxies a los servicios necesarios"""

        self.obtainRepository()
        self.obtainBlackboard()

    def setCurrentZones (self, zones):
        """Establece el valor de CurrentZones"""
        self.CurrentZones = zones

    def getCurrentZones (self):
        """Devuelve el valor de CurrentZones"""
        return self.CurrentZones
    
    def setCurrentIdWork (self, idWork):
        """Establece el valor de CurrentIdWork"""
        self.CurrentIdWork = idWork

    def getCurrentIdWork (self):
        """Devuelve el valor de CurrentIdWork"""
        return self.CurrentIdWork

    def setCurrentImage (self):
        """Establece el valor de la variable CurrentImage"""
        self.CurrentImage = Util_image.ImageSet()

    def getCurrentImage (self):
        """Devuelve el valor de la variable CurrentImage"""
        return self.CurrentImage

    def addRenderAgent (self, renderAgentName, renderAgent):
        """Añade un nuevo agente"""
        self.RenderAgents[renderAgentName] = renderAgent

    def removeRenderAgent (self, renderAgentName):
        """Elimina un agente"""
        prx = self.RenderAgents.pop(renderAgentName)

    def getRenderAgents (self):
        """Devuelve el valor de RenderAgents"""
        return self.RenderAgents

    def benchmarkValue (self, value, current = None):
        """Incrementa el valor medio del tiempo empleado en la ejecución del benchmark"""
        self.incrementBenchmarkValue(value)    

    def incrementBenchmarkValue (self, value):
        """Incrementa el valor de la variable BenchmarkValue en value"""
        self.BenchmarkValue += value

    def getBenchmarkValue (self):
        """Devuelve el valor de la variable BenchmarkValue"""
        return self.BenchmarkValue

    def addBidding (self, bidding):
        """Añade una puja a la lista de pujas"""
        self.Biddings.append(bidding)

    def getBiddings (self):
        """Devuelve la lista de pujas actuales"""
        return self.Biddings

    def setInitialBidding (self, value):
        self.InitialBidding = value

    def getInitialBidding (self):
        return self.InitialBidding

    def clearBiddings (self):
        """Elimina las pujas existentes"""
        self.Biddings = []

    def setNumberOfPieces (self, value):
        """Establece el valor de la variable NumberOfPieces"""
        self.NumberOfPieces = value

    def incrementNumberOfPieces (self):
        """Incrementa en una unidad el valor de la variable NumberOfPieces"""
        self.NumberOfPieces += 1

    def getNumberOfPieces (self):
        """Establece el valor de la variable NumberOfPieces"""
        return self.NumberOfPieces

    def setCurrentBiddingTime (self, time):
        """Establece el valor de la variable CurrentBiddingTime"""
        self.CurrentBiddingTime = time

    def incrementCurrentBiddingTime (self, time):
        """Incrementa el valor de la variable CurrentBiddingTime"""
        self.CurrentBiddingTime += time

    def getCurrentBiddingTime (self):
        """Devuelve el valor de la variable CurrentBiddingTime"""
        return self.CurrentBiddingTime

    def setLog (self, string):
        """Establece el valor de la variable Log"""
        self.Log = string

    def addLog (self, string):
        """Actualiza el log"""
        self.Log += string

    def getLog (self, current = None):
        """Devuelve el valor de la variable Log"""
        return self.Log

    def setFinalTimes (self, string):
        """Establece el valor de la variable FinalTimes"""
        self.FinalTimes = string

    def addFinalTimes (self, string):
        """Actualiza el valor de la variable FinalTimes"""
        self.FinalTimes += string

    def getFinalTimes (self, current = None):
        """Devuelve el valor de la variable FinalTimes"""
        return self.FinalTimes

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
            print self.getServiceId() + ' --> No pudo obtener un proxy al repositorio de modelos.'

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
            print self.getServiceId() + ' --> No pudo obtener un proxy a la pizarra.'

    def subscribe (self, renderAgentName, renderAgent, current = None):
        """Permite que un agente especializado en el render se subscriba al Master"""

        print self.getServiceId() + ' --> Nuevo agente subscrito: ' + renderAgentName + '.'
        self.addRenderAgent(renderAgentName, renderAgent)

    def unsubscribe (self, renderAgentName, current = None):
        """Permite que un agente especializado en el render se dé de baja con el Master"""

        print self.getServiceId() + '--> El agente ' + renderAgentName + ' se da de baja.'
        self.removeRenderAgent(renderAgentName)

    def notifyNewWork (self, zones, idWork, optimization, current = None):
        """Obtiene la información asociada a un trabajo: zones representa la división en zonas e idWork es el id del trabajo"""

        self.setLog('')
        self.setFinalTimes('')
        self.addLog('NewWork: ' + str(idWork) + '\n')
        self.setCurrentBiddingTime(0)
        self.setInitialBidding(0)
        # Obtención de los proxies a los servicios necesarios.
        self.obtainProxies()
        # Limpieza de la pizarra y de las anteriores apuestas.
        self.getBlackboard().clear()
        self.clearBiddings()
        # Se establecen los valores para las zonas de trabajo actuales.
        self.setCurrentZones(zones)
        self.setCurrentIdWork(idWork)
        self.setCurrentImage()
        # Aún no ha llegado ningún trozo de la imagen final.
        self.setNumberOfPieces(0)

        # Escritura en la pizarra del nuevo trabajo.
        self.writeWorkInBlackboard(idWork)
        # Notificación de un nuevo trabajo a los agentes subscritos a este Master.
        try:
            benchmarkMedium = int(self.getBenchmarkValue() / len(self.getRenderAgents()))
        except ZeroDivisionError:
            print 'No existen agentes subscritos...'
        self.notifyNewWorkToAgents(zones, idWork, benchmarkMedium)
        # Reparto inicial de las zonas del trabajo actual entre los agentes especializados en render subscritos.
        self.initialDistribution(optimization)

    def notifyNewWorkToAgents (self, zones, idWork, benchmarkValue):
        """Notifica un nuevo trabajo a los agentes subscritos al master"""

        for prxAgent in self.getRenderAgents().values():
            prxAgent.notifyNewWork(zones, idWork, benchmarkValue)

    def initialDistribution (self, optimization):
        """Lleva a cabo la distribución inicial de zonas entre los agentes especializados en el render"""

        # Se distribuyen los trozos a los agentes para el render tamaño "sello".
        # La distribución se hace en grupos de trozos.
        zonesPerBlock = max(int(len(self.getCurrentZones()) / len(self.getRenderAgents())), 1)
        
        for a in range(len(self.getRenderAgents())):

            if a <> len(self.getRenderAgents()) - 1:
                zones = self.getCurrentZones()[a * zonesPerBlock: (a + 1) * zonesPerBlock]
            else:
                zones = self.getCurrentZones()[a * zonesPerBlock: len(self.getCurrentZones())]

            agentPrx = self.getRenderAgents().values()[a]
            cb = AMI_Model_notifyZonesI()
            agentPrx.notifyZones_async(cb, zones, self.getCurrentIdWork(), optimization)
        
        # Comienza el proceso de subasta (se notifica a todos los agentes suscritos).
        self.beginRenderProcess()

    def beginRenderProcess (self):
        """Notifica a los agentes subscritos el comienzo del render final"""

        # Esperamos a que todos los agentes hayan estimado sus trozos.
        while True:
            if self.getBlackboard().isWorkPartiallyEstimated():
                break
            else:
                time.sleep(5)

        # Comienza el proceso de render final.
        for agentPrx in self.getRenderAgents().values():
            agentPrx.beginRenderProcess()

    def bidHigher (self, agent, idWork, idZone, credits, historic, current = None):
        """Estudia la puja de un agente"""

        begin = time.time()
        
        # NOASIGNED indica que la puja todavía no ha sido confirmada.
        bidding = Bidding(agent, idWork, idZone, credits, historic, NOASIGNED)
        self.addBidding(bidding)
        self.addLog('Bidding ==> ' + bidding.__str__() + '\n')
        # Si todos los agentes disponibles han apostado, se realiza el reparto de zonas en función de las características de los agentes.
        print 'MASTER --> Apuestas: '  + str(len(self.getBiddings())) + 'Agentes apostando: ' + str(self.getNumberFreeAgents())
        ##if self.getInitialBidding() == 0:
        if self.getInitialBidding() < len(self.getRenderAgents().values()):
            if len(self.getBiddings()) == self.getNumberFreeAgents():
                self.shareOutZones()
                ##self.setInitialBidding(1)
                self.setInitialBidding(self.getInitialBidding() + 1)
        else:
            self.shareOutZones()

        # Actualización del tiempo empleado en las pujas-asignaciones.
        end = time.time()
        self.incrementCurrentBiddingTime(int(end - begin))

    def getNumberFreeAgents (self):
        """Devuelve el número de agentes ocupados"""

        n = 0

        for agentPrx in self.getRenderAgents().values():
            #if agentPrx.getState() == MASYRO.StateRenderAgent.Resting:
            if agentPrx.getState() == MASYRO.StateRenderAgent.Bidding:
                n += 1

        return n

    def shareOutZones (self):
        """Reparte zonas a los agentes en función de las pujas"""

        print 'Reparto de zonas... Apuestas: ' + str(len(self.getBiddings()))

        done = False
        rendersInfo = []

        # Recorrido de las distintas pujas...
        for i in range(len(self.getBiddings())):
            if self.getBiddings()[i].getState() == NOASIGNED:
                # Suponemos que la puja i es la mejor de momento.
                best = i
                done = True
                
                # Comparación de la puja i con el resto...
                for j in range(len(self.getBiddings())):
                    # Estudio de una misma puja por parte de dos agentes.
                    idWork1, idWork2 = self.getBiddings()[i].getIdWork(), self.getBiddings()[j].getIdWork()
                    idZone1, idZone2 = self.getBiddings()[i].getIdZone(), self.getBiddings()[j].getIdZone()
                    state1, state2 = self.getBiddings()[i].getState(), self.getBiddings()[j].getState()

                    # Si pujan por la misma zona se asigna al agente que ofrece la mejor oferta.
                    if idWork1 == idWork2 and idZone1 == idZone2 and state2 == NOASIGNED:
                        # La mejor oferta será del agente con mayor número de créditos y mejor histórico.
                        v1 = self.getBiddings()[best].getCurrentHistoric()
                        v2 = self.getBiddings()[j].getCurrentHistoric()
                        v1 += self.getBiddings()[best].getCredits()
                        v2 += self.getBiddings()[j].getCredits()
                        if v1 < v2:
                            best = j

            # Si se ha llevado a cabo alguna puja...
            if done:
                done = False
                # La mejor apuesta se asigna al agente que la realizó.
                self.getBiddings()[best].setState(ASIGNED)
                # El resto de pujas de los demás agentes para la misma zona se descartan.
                self.markWithoutPossibility(best)
                # El master escribe en la pizarra que el agente se hace cargo del trozo.
                a, b, c = self.getCurrentIdWork(), self.getBiddings()[best].getIdZone(), self.getBiddings()[best].getAgent()
                self.getBlackboard().setWorkUnit(a, b, c)
                # Se añade la información para el posterior render.
                rendersInfo.append(RenderInfo(a, b, c))

        # Actualizamos para la siguiente puja.
        self.markWithPossibility()

        # Se ordenan los renders a los agentes, y al resto se les solicita que pujen de nuevo.
        for b in self.getBiddings():
            if self.isInListOfRenders(b.getAgent(), rendersInfo):
                self.addLog('Rendering ==> ' + b.__str__() + '\n')
                self.orderRender(b.getIdWork(), b.getIdZone(), b.getAgent())
            else:
                self.orderNewBidding(b.getAgent())

        # Se eliminan las anteriores pujas.
        self.clearBiddings()

    def isInListOfRenders (self, agent, rendersInfo):
        """Indica si agent pertence a la lista rendersInfo"""

        for r in rendersInfo:
            if r.getAgent() == agent:
                return True

        return False

    def markWithoutPossibility (self, best):
        """Marca todas las pujas asociadas al mismo trozo que el trozo ganador como no posibles en la ronda actual"""

        for x in self.getBiddings():
            if x.getIdWork() == self.getBiddings()[best].getIdWork() and x.getIdZone() == self.getBiddings()[best].getIdZone() and x.getState() == NOASIGNED:
                x.setState(WITHOUTPOSSIBILITY)

    def markWithPossibility (self):
        """Actualiza todas las pujas para la siguiente puja"""

        for x in self.getBiddings():
            if x.getState() == WITHOUTPOSSIBILITY:
                x.setState(NOASIGNED)

    def orderRender (self, idWork, idZone, agent):
        """Comunica al agente agent que renderice la zna idZone del trabajo idWork"""

        agentPrx = self.getRenderAgents()[agent]
        cb = AMI_Model_renderI()
        agentPrx.render_async(cb, idWork, idZone, agent)

    def orderNewBidding (self, agent):
        """Comunica al agente agent que vuelva a pujar por un trozo"""

        agentPrx = self.getRenderAgents()[agent]
        agentPrx.beginRenderProcess()

    def noMoreBiddings (self, current = None):
        """Indica la finalización del trabajo"""

        if self.getBlackboard().isCurrentWorkFinished():
            self.addLog('\n\n' + self.getBlackboard().show() + '\n\n')
            self.addFinalTimes('AnalysisTime: ' + str(self.getBlackboard().getAnalysisTime()) + '\n')
            self.addFinalTimes('EstimatedRenderTime: ' + str(self.getBlackboard().getEstimatedRenderTime()) + '\n')
            self.addFinalTimes('BiddingTime: ' + str(self.getCurrentBiddingTime()) + '\n\n')
            self.addFinalTimes(self.getBlackboard().getTimeCurrentWorks())
            f = open(LOG, 'w')
            f.write(self.getLog())
            f.write(self.getFinalTimes())
            f.close()

            for x in self.getRenderAgents().values():
                print x.getState()

    def giveFinalImage (self, idWork, idZone, partialImage, x1, y1, x2, y2, ibs, current = None):
        """Permite obtener un trozo de la imagen final"""

        # Se guarda el trozo recibido como una imagen.
        print 'Imagen [' + str(idWork) + ', ' + str(idZone) + ']'
        path = os.path.join(MASTER_WORK_DIR, str(idWork) + '_' + str(idZone) + EXT)
        array.array('B', partialImage).tofile(open(path, 'w'))

        # Se crea un objeto de tipo PieceOfImage por cada trozo recibido y se añade al recurso que maneja la imagen actual.
        self.getCurrentImage().add(idZone, Util_image.PieceOfImage(x1, y1, x2, y2, ibs))
        self.incrementNumberOfPieces()

        # En cada paso se realiza la construcción de la imagen de salida final.
        finalImage = Image.open(path)
        pathF = os.path.join(MASTER_WORK_DIR, SALIDA)
        finalImage.save(pathF)
        resX, resY = finalImage.size

        # Averiguamos el número de vecinos de cada pieceOfImage.
        for i in self.getCurrentImage().getImages().values():
            i.setResX(resX)
            i.setResY(resY)
            self.getCurrentImage().setNeighbourhood(i)

        # Composición final.
        self.finalComposition(idWork, finalImage)

    def finalComposition (self, idWork, finalImage):
        """Lleva a cabo la composición final de la imagen"""
        
        for x in self.getCurrentImage().getImages().items():

            for y in self.getCurrentImage().getImages().items():
                    
                # Se comprueba si y es el vecino derecho de x.
                t, limite = x[1].isRightNeighbour(y[1])
                if t and x[1].getRightNeighbour() > 0:

                    # Actualización de vecinos.
                    x[1].setRightNeighbour(x[1].getRightNeighbour() - 1)
                    y[1].setLeftNeighbour(y[1].getLeftNeighbour() - 1)

                    path1 = os.path.join(MASTER_WORK_DIR, str(idWork) + '_' + str(x[0]) + EXT)
                    path2 = os.path.join(MASTER_WORK_DIR, str(idWork) + '_' + str(y[0]) + EXT)
                    im1 = Image.open(path1)
                    im2 = Image.open(path2)
                    # finalIbs es el valor final de la banda de interpolación.
                    finalIbs = min(x[1].getIbs(), y[1].getIbs())
                    # Limitex representa el trozo a interpolar de x.
                    limitex = (limite[0] - finalIbs, limite[1], limite[2], limite[3])
                    # Limitey representa el trozo a interpolar de y.
                    limitey = (limite[0], limite[1], limite[2] + finalIbs, limite[3])
                    # LimiteFinal representa todo el trozo a interpolar.
                    limiteFinal = (limitex[0], limitex[1], limitey[2], limitey[3])

                    # Se pegan los dos trozos.
                    boxX = (x[1].getX1(), x[1].getY1(), x[1].getX2(), x[1].getY2())
                    regionX = im1.crop(boxX)
                    boxY = (y[1].getX1(), y[1].getY1(), y[1].getX2(), y[1].getY2())
                    regionY = im2.crop(boxY)
                    finalImage.paste(regionX, boxX)
                    finalImage.paste(regionY, boxY)

                    # Se actualiza la vecindad de los trozos.
                    imI = im1.crop(limiteFinal)
                    imD = im2.crop(limiteFinal)
                    mask = Util_image.createMask(limiteFinal[2] - limiteFinal[0], limiteFinal[3] - limiteFinal[1])
                    im3 = Image.composite(imI, imD, mask)
                    finalImage.paste(im3, limiteFinal)

        # Almacenamiento de la imagen final.
        pathF = os.path.join(MASTER_WORK_DIR, SALIDA)
        finalImage.save(pathF)
        Util_image.createLowResolutionImage(MASTER_WORK_DIR, SALIDA, MASYRO_WEB_DIR)

    def showAgentStates (self, current = None):

        straux = ''

        for agent in self.getRenderAgents().items():
            straux += (agent[0] + ':' + str(agent[1].getState()) + '\n')

        return straux

    def writeWorkInBlackboard (self, idWork):
        """Escribe la información del trabajo actual en la pizarra"""

        # Se escriben los registros asociados a las distintas zonas.
        for x in self.getCurrentZones():
            size = (x.y2 - x.y1) * (x.x2 - x.x1)
            register = MASYRO.TRegister(idWork, x.id, int(size), int(x.m), 0, 0, '', MASYRO.StateRegister.NotDone, 0, 0, 0)
            self.getBlackboard().write(register)

    def registerAsWKO (self):
        """Registra al Master como un objeto bien conocido"""

        properties = self.communicator().getProperties()
        adapter = self.communicator().createObjectAdapter('MasterAdapter')
        id = Ice.stringToIdentity(properties.getProperty('IdentityMA'))

        self.init(properties.getProperty('InputMA'))

        adapter.add(self, id)
        adapter.activate()

    def clear (self):
        """Libera recursos asociados al master"""

        os.system('rm -f ' + LOG)

    def run (self, args):
        """Ejecución del código asociado al master"""

        self.shutdownOnInterrupt()

        self.registerAsWKO()

	self.communicator().waitForShutdown()

        # Liberación de recursos.
        self.clear()

	return 0

MasterI().main(sys.argv, 'config/localServices.cfg')
