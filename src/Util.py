#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern醤dez ************************#
#************************************************************#

import zipfile, os
import Ice
Ice.loadSlice('../FIPA/FIPA.ice', ['-I' '/usr/share/slice'])
import FIPA

def getFileName (namelist, ext):
    """Devuelve el nombre del archivo de namelist cuya extension se corresponde con ext"""

    for f in namelist:
        r = f.split('.')
        if len(r) == 2 and r[1] == ext:
            return f

    return None

def createInput (file, complexity, neighbourDifference, size):
    """Crea un fichero de texto a partir de la informaci贸n de values"""

    f = open(file, 'w')

    for k in complexity.keys():
        f.write('C ' + str(k) + ' ' + str(complexity[k][0]) + ' ' + str(complexity[k][1]) + ' ' + str(complexity[k][2]) + ' ' + str(complexity[k][3]) + '\n')
    for k in neighbourDifference.keys():
        f.write('Nd ' + str(k) + ' ' + str(neighbourDifference[k][0]) + ' ' + str(neighbourDifference[k][1]) + ' ' + str(neighbourDifference[k][2]) + ' ' + str(neighbourDifference[k][3]) + '\n')
    for k in size.keys():
        f.write('S ' + str(k) + ' ' + str(size[k][0]) + ' ' + str(size[k][1]) + ' ' + str(size[k][2]) + ' ' + str(size[k][3]) + '\n')

    f.close()

def loadInput (file):
    """Devuelve un diccionario a partir del fichero file"""

    s, c, nd = {}, {}, {}

    f = open(file)
    
    for x in f:
        y = x.split()
        if y[0] == 'C':
            c[y[1]] = (y[2], y[3], y[4], y[5])
        elif y[0] == 'S':
            s[y[1]] = (y[2], y[3], y[4], y[5])
        elif y[0] == 'Nd':
            nd[y[1]] = (y[2], y[3], y[4], y[5])

    f.close()

    return s, c, nd

def getSize (idZone, zones):
    """Devuelve el tama帽o de la zona idZone delimitada por (x1, y1), (x2, y2)"""

    for z in zones:
        if idZone == z.id:
            return (z.x2 - z.x1) * (z.y2 - z.y1)

    return -1

def getZoneSize(x1, y1, x2, y2):
    """Devuelve el tama帽o de la zona delimitada por (x1, y1), (x2, y2)"""
    return (x2 - x1) * (y2 - y1)

def traduceState (state):
    """Obtiene la representaci贸n textual asociada a state"""

    if state == 0:
        return 'Initiated'
    elif state == 1:
        return 'Active'
    elif state == 2:
        return 'Suspended'
    elif state == 3:
        return 'Waiting'
    elif state == 4:
        return 'Transit'
    else:
        return ''

def traduceExplanation (explanation):
    """Obtiene la representaci贸n textual asociada a explanation"""

    if explanation == 1:
        return 'Duplicate'
    elif explanation == 2:
        return 'Access'
    elif explanation == 3:
        return 'Invalid'
    elif explanation == 4:
        return 'Success'
    elif explanation == 5:
        return 'NotFound'
    else:
        return ''

class Zip:
    """La clase Zip representa a un archivo comprimido en formato zip"""

    # name representa la ruta del archivo .zip.
    def __init__ (self, name):
        """Crea un objeto del tipo Zip"""
        
        self.Name = name + 'zip'
        #os.chdir('render')
        self.File = zipfile.ZipFile(self.Name, 'w', zipfile.ZIP_DEFLATED)
        #os.chdir('..')

    def getName (self):
        """Devuelve el nombre del archivo"""
        return self.Name

    def getFile (self):
        """Devuelve el archivo ya comprimido"""
        return self.File

    def add (self, file):
        """A帽ade el archivo representado por file al archivo comprimido"""

        #os.chdir('render')
        self.getFile().write(file)
        #os.chdir('..')

    def close (self):
        """Cierra el archivo"""
        self.getFile().close()
    
class Unzip:
    """La clase Unzip representa la funcionalidad asociada a la descompresi贸n de un archivo en formato zip"""

    def __init__ (self, name):
        """Crea un objeto del tipo Unzip"""

        self.Name = name
        self.File = zipfile.ZipFile(self.Name, 'r')

    def getName (self):
        """Devuelve el nombre del archivo"""
        return self.Name

    def getFile (self):
        """Devuelve el archivo comprimido"""
        return self.File

    def extract (self, extractDir = './render'):
        """Extrae los archivos del archivo comprimido y devuelve una lista con los nombres de dichos archivos"""

        os.chdir(extractDir)
        for x in self.getFile().namelist():
            outfile = file(x, 'w')
            outfile.write(self.getFile().read(x))
            outfile.flush()
            outfile.close()
        os.chdir('..')

        return self.getFile().namelist()
