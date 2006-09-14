#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Author: David Vallejo Fern·ndez ***********************#
#************************************************************#

import sys, os, math, time, array
import Ice
import Image, ImageDraw
Ice.loadSlice('../MASYRO/MASYRO.ice', ['-I' '/usr/share/slice'])
import MASYRO
import Agent, Zone, Service
import Util
from Agent import *
from Zone import *
from Service import *

# Factores que indican la anchura y la altura mÌnima del trozo m·s pequeÒo permitido.
FACTOR_X_MIN, FACTOR_Y_MIN = 6, 4
# Factores de divisiÛn de zonas en el proceso final de ajuste.
FACTOR_DIV1, FACTOR_DIV2 = 1.5, 3
# Valor de la desviaciÛn est·ndar permitida para el color de un trozo.
DESV = 30.0
# Color de las lÌneas que delimitan las zonas de una imagen.
LEVEL1 = 255
LEVEL2 = 175
LEVEL3 = 100
# Valor que representa la diferencia m·xima entre la media del color de una zona.
MAX_COLOUR = 20.0
# Variables que representan los directorios de trabajo para un agente especializado en el an·lisis de la entrada.
FROM_RENDER_DIR = '../src/analyst'
ANALYST_WORK_DIR = './analyst'
RENDER_WORK_DIR = './render'
# Variable que indica el nombre del fichero de salida final.
NAME_OUTPUT_FILE = 'salida.png'

class AnalystI (MASYRO.Analyst, Ice.Application, Service):
    """La clase Analyst representa un servicio especializado en el an·lisis y estudio de una escena"""

    def __init__ (self):
        """Crea un objeto del tipo Analyst"""

        Service.__init__(self)

        # Par·metros necesarios para el tratamiento de la salida del render inicial.
        # InputFile --> Objeto de tipo Image que representa la imagen obtenida del render inicial.
        self.InputFile = None
        # Resoluci√≥n de InputFile.
        self.X, self.Y = 0, 0
        # Level == 1 --> Divisi√≥n est√°ndar Level == 2 --> Divisi√≥n con fusi√≥n Level == 3 --> Divisi√≥n con equilibrado de complejidad.
        self.Level = 0
        # PixelMatrix representa la matriz de p√≠xeles de InputFile.
        self.PixelMatrix = []
        # Listas que representan las zonas de la imagen en funci√≥n del par√°metro Level.
        self.InitialZones, self.MergingZones, self.FinalZones = [], [], []

        # Proxy al agente Master y al repositorio.
        self.Master, self.Repository, self.Blackboard = None, None, None

    def initialRender (self, file):
        """Renderiza el modelo asociado a ficheroBlender"""

        # Se extrae el contenido del archivo comprimido (zip).
        unzip = Util.Unzip(file)
        
        # Se almacenan los nombres de los archivos contenidos en el archivo comprimido.
        nameList = unzip.extract(ANALYST_WORK_DIR)
        # Se obtiene el nombre completo del fichero que alberga la escena.
        scene = Util.getFileName(nameList, 'blend')
        path = os.path.join(ANALYST_WORK_DIR, scene)
        # Render inicial para estimar la complejidad de la escena.
        os.system('blender -b ' + path + ' -P ./InitialRender.py -f 1 ')
        path1 = os.path.join(ANALYST_WORK_DIR, '0001.png')
        path2 = os.path.join(ANALYST_WORK_DIR, NAME_OUTPUT_FILE)
        os.system('mv ' + path1 + ' ' + path2)

    def setInputFile (self, inputFile):
        """Establece el fichero de entrada"""
        self.InputFile = Image.open(inputFile)

    def getInputFile (self):
        """Devuelve el fichero de entrada ya abierto"""
        return self.InputFile

    def getInfoInitialImage (self, inputFile):
        """Abre el fichero de entrada asociado a la imagen y obtiene su tamaÒo"""

        # Apertura de la imagen para su an·lisis.
        self.setInputFile(inputFile)
        # ObtenciÛn de la resoluciÛn de la imagen.
        x, y = self.getInputFile().size
        self.setX(x)
        self.setY(y)
        # CreaciÛn de la matriz de pÌxeles.
        for i in range (self.X):
            aux = []
            for j in range (self.Y):
                aux.append(self.getInputFile().getpixel((i, j)))
            self.addZone(aux, self.getPixelMatrix())

    def setX (self, x):
        """Establece el valor de la variable X"""
        self.X = x

    def getX (self):
        """Devuelve la longitud de la imagen"""
        return self.X

    def setY (self, y):
        """Establece el valor de la variable Y"""
        self.Y = y

    def getY (self):
        """Devuelve la altura de la imagen"""
        return self.Y

    def getSmallestPieceX (self):
        """Devuelve la anchura del trozo m·s estrecho permitido"""
        return self.getX() / FACTOR_X_MIN

    def getSmallestPieceY (self):
        """Devuelve la altura del trozo m·s bajo permitido"""
        return self.getX() / FACTOR_Y_MIN

    def setLevel (self, level):
        """Establece el valor de la variable Level"""
        self.Level = level

    def getLevel (self):
        """Devuelve la variable Level"""
        return self.Level

    def getPixelMatrix (self):
        """Devuelve una lista de listas que representa el color de la imagen"""
        return self.PixelMatrix

    def setPixelMatrix (self, i, j, p):
        """Establece el valor de la coordenada (i, j) de la variable PixelMatrix a p"""
        self.PixelMatrix[i][j] = p

    def getPixelMatrixValue (self, i, j):
        """Devuelve el valor de la coordenada (i, j) de la variable PixelMatrix"""
        return self.PixelMatrix[i][j]

    def addZone (self, zone, zoneList):
        """AÒade una zona a la lista de zonas"""
        zoneList.append(zone)

    def deleteZone (self, zone, zoneList):
        """Elimina una zona de la lista de zonas"""
        zoneList.remove(zone)

    def getInitialZones (self):
        """Devuelve la lista de zonas iniciales"""
        return self.InitialZones

    def getMergingZones (self):
        """Devuelve la lista de zonas ya fusionadas"""
        return self.MergingZones

    def getFinalZones (self):
        """Devuelve la lista de zonas con el ajuste complejidad/tamaÒo"""
        return self.FinalZones

    def getCurrentAnalysisTime (self, current = None):
        """Devuelve el tiempo empleado para el an√°lisis de la escena actual"""
        return self.getAnalysisTime()    

    def getId (self):
        """Obtiene un identificador ˙nico para la zona"""

        if len(self.getInitialZones()) == 0:
            return 0
        else:
            return self.getInitialZones()[len(self.getInitialZones()) - 1].getId() + 1

    def getIdAjuste (self):
        """Obtiene un identificador ˙nico para las nuevas zonas consecuencia del ajuste final"""
        return self.getFinalZones()[len(self.getFinalZones()) - 1].getId() + 1

    def divideZone (self, zone):
        """Divide la zona pasada como par·metro o la almacena como zona no divisible"""

        x1, y1 = zone.getX1(), zone.getY1()
        x2, y2 = zone.getX2(), zone.getY2()
        
        # Estudiamos si es divisible.
        med, d = self.getMediumStandardDesviation(zone)

        # Si la desviaci√≥n est√°ndar es mayor que la establecida y el trozo es lo suficientemente grande, se divide.
        if (d > DESV) and zone.getWidth() > self.getSmallestPieceX() and zone.getHeight() > self.getSmallestPieceY():
            self.divideZone(Zone(-1, x1, y1, x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2))
            self.divideZone(Zone(-1, x1 + (x2 - x1) / 2, y1, x2, y1 + (y2 - y1) / 2))
            self.divideZone(Zone(-1, x1, y1 + (y2 - y1) / 2, x1 + (x2 - x1) / 2, y2))
            self.divideZone(Zone(-1, x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2, x2, y2))
            
        # Si la zona no es divisible, la insertamos en la lista de zonas.
        else:
            zone = Zone(self.getId(), x1, y1, x2, y2)
            zone.setDesv(d)
            zone.setMed(med)
            self.addZone(zone, self.getInitialZones())            

    def dibujarLineasSeparacion (self, ficheroSalida, zonas, fill):
        """Crea una imagen a partir de la imagen original dibujando las zonas especificadas con lÌneas"""

        draw = ImageDraw.Draw(self.getInputFile())
        FILL = fill

        # Se dibujan las lÌneas.
        for x in zonas:
            draw.line((x.getX1(), x.getY1(), x.getX2(), x.getY1()), FILL)
            draw.line((x.getX2(), x.getY1(), x.getX2(), x.getY2()), FILL)
            draw.line((x.getX1(), x.getY1(), x.getX1(), x.getY2()), FILL)
            draw.line((x.getX1(), x.getY2(), x.getX2(), x.getY2()), FILL)

        self.getInputFile().save(ficheroSalida)

        del draw

    def getMediumStandardDesviation (self, zone):
        """Devuelve la media y la desviaciÛn est·ndar de la zona delimitada por x1, y1, x2, y2"""

        sume, numData = 0, 0

        # C·lculo del promedio.
        for i in range (zone.getX1(), zone.getX2()):
            for j in range (zone.getY1(), zone.getY2()):
                sume += self.getPixelMatrixValue(i, j)
                numData += 1

        medium = float(sume) / float(numData)

        # C·lculo de la desviaciÛn est·ndar
        sume = 0
        for i in range (zone.getX1(), zone.getX2()):
            for j in range (zone.getY1(), zone.getY2()):
                sume += math.pow((self.getPixelMatrixValue(i, j) - medium), 2)

        desv = math.sqrt(float(sume) / float(numData))

        return medium, desv        

    def fusion (self):
        """Une zonas adyacentes de complejidad semejante"""

        change = True

        # Inicializamos la lista de zonas resultantes con las zonas iniciales.
        for x in self.getInitialZones():
            self.addZone(x, self.getMergingZones())

        # Mientras haya cambios seguimos estudiando la lista de zonas.
        while change:
            change = False
            for x in self.getMergingZones():
                for y in self.getMergingZones():
                    # Si tenemos dos zonas con una media de color parecido...
                    if math.fabs(x.getMed() - y.getMed()) < MAX_COLOUR:
                        # Llamada a funciÛn de adyacencia, encargada de insertar la nueva zona en su caso.
                        aux = self.adjacency(x, y)
                        if aux == True:
                            change = True

    def adjacency (self, x, y):
        """Comprueba si dos zonas son adyacentes y en tal caso las fusiona dejando sÛlo una"""

        # Se comprueba la adyacencia vertical.
        if (x.getX1() == y.getX1()) and (x.getY2() == y.getY1()) and (x.getX2() == y.getX2()):
            # Se fusionan creando una nueva, cambiando el valor de la coordenada y2.
            x.setY2(y.getY2())
            self.deleteZone(y, self.getMergingZones())

        # Se comprueba la adyacencia horizontal.
        elif (x.getX2() == y.getX1()) and (x.getY1() == y.getY1()) and (x.getY2() == y.getY2()):
            # Se fusionan creando una nueva, cambiando el valor de la coordenada x2.
            x.setX2(y.getX2())
            medium, d = self.getMediumStandardDesviation(x)
            x.setMed(medium)
            x.setDesv(d)
            self.deleteZone(y, self.getMergingZones())

        else:
            return False

        return True

    def balance (self):
        """Divide zonas a partir de la lista MergingZones en funciÛn de un ratio complejidad/tamaÒo"""

        # Lista con las complejidades de cada una de las zonas, en funciÛn de su color.
        complexity = []
        aux = []

        # Inicializamos la lista de zonas resultantes con las zonas tras la fusiÛn.
        for x in self.getMergingZones():
            self.addZone(x, self.getFinalZones())

        for x in self.getFinalZones():
            c = 0
            for i in range(x.getX1(), x.getX2() - 1):
                for j in range(x.getY1(), x.getY2() - 1):
                    c += self.getPixelMatrix()[i][j]
            complexity.append(c / x.getSize())

        medium, desv = self.getStandardDesviationBalance(complexity)

        for i in range(len(complexity)):
            if (medium) <= complexity[i]:
                zona = self.getFinalZones()[i]
                self.divideFinalZone(zona, medium)
                aux.append(zona)

        for x in aux:
            self.deleteZone(x, self.getFinalZones())
                
    def getStandardDesviationBalance (self, complexity):
        """Devuelve la media y la desviaciÛn est·ndar de cada zona con respecto a todas las zonas"""

        sume, numData = 0, 0

        # C·lculo del promedio.
        for x in complexity:
            sume += x
            numData += 1

        medium = float(sume) / float(numData)

        # C·lculo de la desviaciÛn est·ndar
        sume = 0
        for x in complexity:
            sume += math.pow((x - medium), 2)

        desv = math.sqrt(float(sume) / float(numData))

        return medium, desv

    def divideFinalZone (self, zone, med):
        """Divide una zona en el proceso de ajuste final"""

        # Se elimina la zona compleja, seg˙n el ratio complejidad/tamaÒo.
        x1, y1 = zone.getX1(), zone.getY1()
        x2, y2 = zone.getX2(), zone.getY2()
        
        # Se aÒade una zona que constituye la mitad de la zona eliminada.
        z1 = Zone(self.getIdAjuste(), x1, y1, x2, y1 + (y2 - y1) / 2)
        medium, d = self.getMediumStandardDesviation(z1)
        z1.setMed(medium)
        z1.setDesv(d)
        self.addZone(z1, self.getFinalZones())

        # Se aÒade una zona que constituye la otra mitad de la zona eliminada.
        z2 = Zone(self.getIdAjuste(), x1, y1 + (y2 - y1) / 2, x2, y2)
        medium, d = self.getMediumStandardDesviation(z2)
        z2.setMed(medium)
        z2.setDesv(d)
        self.addZone(z2, self.getFinalZones())
        
        # Si la zona en cuestiÛn est· por encima del doble de la media...
        if (zone.getMed() >= med * FACTOR_DIV1):

            x1, y1 = z1.getX1(), z1.getY1()
            x2, y2 = z1.getX2(), z1.getY2()
            # Se aÒade una zona que constituye la mitad vertical izquierda de la zona eliminada.
            zvi = Zone(self.getIdAjuste(), x1, y1, x1 + (x2 - x1) / 2, y2)
            medium, d = self.getMediumStandardDesviation(zvi)
            zvi.setMed(medium)
            zvi.setDesv(d)
            self.addZone(zvi, self.getFinalZones())
            # Se aÒade una zona que constituye la mitad vertical derecha de la zona eliminada.
            zvd = Zone(self.getIdAjuste(), x1 + (x2 - x1) / 2, y1, x2, y2)
            medium, d = self.getMediumStandardDesviation(zvd)
            zvd.setMed(medium)
            zvd.setDesv(d)
            self.addZone(zvd, self.getFinalZones())
            # Se elimina la zona original.
            self.deleteZone(z1, self.getFinalZones())

            x1, y1 = z2.getX1(), z2.getY1()
            x2, y2 = z2.getX2(), z2.getY2()
            # Se aÒade una zona que constituye la mitad vertical izquierda de la zona eliminada.
            zvi = Zone(self.getIdAjuste(), x1, y1, x1 + (x2 - x1) / 2, y2)
            medium, d = self.getMediumStandardDesviation(zvi)
            zvi.setMed(medium)
            zvi.setDesv(d)
            self.addZone(zvi, self.getFinalZones())
            # Se aÒade una zona que constituye la mitad vertical derecha de la zona eliminada
            zvd = Zone(self.getIdAjuste(), x1 + (x2 - x1) / 2, y1, x2, y2)
            medium, d = self.getMediumStandardDesviation(zvd)
            zvd.setMed(medium)
            zvd.setDesv(d)
            self.addZone(zvd, self.getFinalZones())
            # Se elimina la zona original.
            self.deleteZone(z2, self.getFinalZones())

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
            print self.getServiceId() + ' --> Fue incapaz de obtener un proxy a un Master.'
            return False

    def setBlackboard (self, blackboard):
        """Establece un proxy al servicio Blackboard"""
        self.Blackboard = blackboard

    def getBlackboard (self):
        """Devuelve un proxy al servicio Blackboard"""
        return self.Blackboard

    def obtainBlackboard (self):
        """Obtiene un proxy al servicio Blackboard"""

        try:
            obj = self.communicator().stringToProxy('blackboard')
            self.setBlackboard(MASYRO.BlackboardPrx.checkedCast(obj))
            
        except Ice.NotRegisteredException:
            proxy = self.communicator().getProperties().getProperty('IceGrid.InstanceName') + '/Query'
            query = IceGrid.QueryPrx.checkedCast(self.communicator().stringToProxy(proxy))
            self.setBlackboard(MASYRO.BlackboardPrx.checkedCast(query.findObjectByType('::MASYRO::Blackboard')))

        except Ice.LocalException:
            print self.getServiceId() + ' --> No pudo obtener un proxy al servicio Blackboard.'

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

    def notifyNewWorkToMaster (self, idWork, optimization):
        """Notifica la existencia de un nuevo trabajo al Master, encargado de la gestiÛn del mismo"""

        if self.obtainMaster():
            print self.getServiceId() + ' --> Master obtenido...'
            zones = []
            for x in self.getZones(self.getLevel()):
                zones.append(MASYRO.TZone(x.getId(), x.getX1(), x.getY1(), x.getX2(), x.getY2(), x.getDesv(), x.getMed()))
            self.getMaster().notifyNewWork(zones, idWork, optimization)
            print self.getServiceId() + ' --> Notificado nuevo trabajo al Master.'

        else:
            print self.getServiceId() + ' --> No se pudo obtener una referencia al Master.'

    def sendModelToRepository (self, zip, file):
        """EnvÌa un nuevo modelo al Repositorio"""

        try:
            self.obtainRepository()
            return self.getRepository().put(zip, file)

        except Ice.MemoryLimitException:
            print self.getServiceId() + ' --> Se excediÛ la memoria del ModelRepository'

    def mostrarPixelMatrix (self):
        """Muestra el tablero asociado a la salida del render inicial"""

        for i in range (0, self.getY()):
            aux = ''
            for j in range (0, self.getX()):                
                aux += self.getPixelMatrixValue(j, i).__str__() + ' '
            print aux

    def mostrarZones (self):
        """Muestra las zonas resultantes de la divisiÛn inicial --> Zona i: (x1, y1, x2, y2, complejidad)"""
        
        for x in self.getInitialZones():
            print x
        print 'N˙mero de zonas sin fusionar: ', len(self.getInitialZones())

    def mostrarMergingZones (self):
        """Muestra las zonas resultantes de la fusiÛn"""
        
        for x in self.getMergingZones():
            print x
        print 'N˙mero de zonas fusionadas: ', len(self.getMergingZones())

    def mostrarFinalZones (self):
        """Muestra las zonas resultantes del equilibrio de la tercera pasada"""
        
        for x in self.getFinalZones():
            print x
        print 'N˙mero de zonas tras el ajuste: ', len(self.getFinalZones())        

    def analyze (self):
        """Lleva a cabo el an·lisis de la escena, en funciÛn del n˙mero de pasadas"""

        if self.getLevel() >= 1:
            self.divideZone(Zone(-1, 0, 0, self.getX(), self.getY()))
        if self.getLevel() >= 2:
            self.fusion()
        if self.getLevel() >= 3:
            self.balance()

    def draw (self):
        """Crea una imagen y la divide en zonas, en funciÛn del n˙mero de pasadas"""

        if self.getLevel() == 1:
            self.dibujarLineasSeparacion(os.path.join(ANALYST_WORK_DIR, 'lineas.png'), self.getInitialZones(), LEVEL1)
        elif self.getLevel() == 2:
            self.dibujarLineasSeparacion(os.path.join(ANALYST_WORK_DIR, 'lineasFusion.png'), self.getMergingZones(), LEVEL2)
        elif self.getLevel() == 3:
            self.dibujarLineasSeparacion(os.path.join(ANALYST_WORK_DIR, 'lineasAjuste.png'), self.getFinalZones(), LEVEL3)

    def getZones (self, level):
        """Devuelve la lista de zonas en funciÛn del par·metro -p"""

        if self.getLevel() == 1:
            return self.getInitialZones()
        elif self.getLevel() == 2:
            return self.getMergingZones()
        elif self.getLevel() == 3:
            return self.getFinalZones()

    def showZones (self):
        """Muestra la lista de zonas en funciÛn del par·metro -p"""

        if self.getLevel() == 1:
            self.mostrarZones()
        elif self.getLevel() == 2:
            self.mostrarMergingZones()
        elif self.getLevel() == 3:
            self.mostrarFinalZones()

    def registerAsWKO (self):
        """Registra al Analyst como un objeto bien conocido"""

        properties = self.communicator().getProperties()
        adapter = self.communicator().createObjectAdapter('AnalystAdapter')
        id = Ice.stringToIdentity(properties.getProperty('IdentityAN'))

        self.init(properties.getProperty('InputAN'))

        adapter.add(self, id)
        adapter.activate()

    def processWork (self, work, workName, level, optimization, current = None):
        """Lleva a cabo un trabajo de rendering"""

        begin = time.time()
        self.clear()

        print 'Procesando ' + workName + '...'
        print 'Nivel de particionado ' + str(level) + '.'
        print 'Nivel de optimizacion ' + str(optimization) + '.\n'

        self.setLevel(level)
        # Se guarda el archivo recibido.
        newWork = array.array('B', open(work).read()).tolist()
        path = os.path.join(ANALYST_WORK_DIR, workName)
        array.array('B', newWork).tofile(open(path, 'w'))
        
        # Render inicial para estimar la complejidad de la escena.
        self.initialRender(path)
        self.getInfoInitialImage(os.path.join(ANALYST_WORK_DIR, NAME_OUTPUT_FILE))
        # Se analiza la imagen obtenida del render inicial para diferenciar las distintas zonas de trabajo.
        self.analyze()
        # Se crea una imagen con las distintas zonas de trabajo.
        self.draw()
        self.showZones()

        end = time.time()
        self.obtainBlackboard()
        self.getBlackboard().setAnalysisTime(int(end - begin))

        # Se env√≠a el trabajo al repositorio y se notifica al Master.
        id = self.sendModelToRepository(workName, newWork)
        self.notifyNewWorkToMaster(id, optimization)
        ### FIN ACCIONES ESPEC√çFICAS.

    def clear (self):
        """Inicializa variables de clase"""

        # Listas que representan las zonas de la imagen en funci√≥n del par√°metro Level.
        self.InitialZones, self.MergingZones, self.FinalZones = [], [], []

    def run (self, args):
        """EjecuciÛn del cÛdigo asociado al analista"""
                
        self.shutdownOnInterrupt()

        self.registerAsWKO()

	self.communicator().waitForShutdown()
        
	return 0

AnalystI().main(sys.argv, 'config/localServices.cfg')
