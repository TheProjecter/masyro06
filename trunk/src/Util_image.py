#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image
import os, os.path, PIL.Image
import array

def createMask(width, height):
    """Returns a mask width x height."""
        
    s=""
    
    offset = 255.0 / width
    data = []
    for i in range(0, width):
        data.append(i*offset)
        
    for i in range(0,height):
        s += array.array("I", data).tostring()
                    
    mask = PIL.Image.fromstring('RGBA', (width,height), s)
    return mask

def createLowResolutionImage (pathToImage, fileName, finalPath):

    newFileName = fileName.split('.')[0] + '.jpg'
    image = Image.open(os.path.join(pathToImage, fileName))
    out = image.resize((300, 240))
    image.save(os.path.join(finalPath, newFileName), 'JPEG')
    out.save(os.path.join(finalPath, 'small' + newFileName), 'JPEG')

class PieceOfImage:
    """La clase PieceOfImage representa un trozo de la imagen"""

    def __init__ (self, x1, y1, x2, y2, ibs):
        """Crea un objeto de tipo PieceOfImage"""

        # Coordenadas de la zona.
        self.X1, self.Y1 = x1, y1
        self.X2, self.Y2 = x2, y2
        # Resolución de la imagen final.
        self.ResX, self.ResY = 0, 0
        # Tamaño de la banda de interpolación de la zona.
        self.Ibs = ibs
        # Neighbours indica si se ha realizado la interpolación con los vecinos.
        # Ej. Neighbours['L'] == 1 ==> Un vecino por la izquierda.
        self.Neighbours = {}
        self.Neighbours['L'], self.Neighbours['R'] = 0, 0
        self.Neighbours['U'], self.Neighbours['D'] = 0, 0

    def getX1 (self):
        """Devuelve el valor de la coordenada X1"""
        return self.X1

    def getY1 (self):
        """Devuelve el valor de la coordenada Y1"""
        return self.Y1

    def getX2 (self):
        """Devuelve el valor de la coordenada X2"""
        return self.X2

    def getY2 (self):
        """Devuelve el valor de la coordenada Y2"""
        return self.Y2

    def getXSize (self):
        """Devuelve la anchura del trozo"""
        return self.getX2() - self.getX1()

    def getYSize (self):
        """Devuelve la altura del trozo"""
        return self.getY2() - self.getY1()    

    def setResX (self, resX):
        """Establece el valor de la variable ResX"""
        self.ResX = resX

    def getResX (self):
        """Devuelve el valor de la variable ResX"""
        return self.ResX

    def setResY (self, resY):
        """Establece el valor de la variable ResY"""
        self.ResY = resY

    def getResY (self):
        """Devuelve el valor de la variable ResY"""
        return self.ResY    

    def getIbs (self):
        """Devuelve el valor del tamaño de la banda de interpolación"""
        return self.Ibs

    def setRightNeighbour (self, v):
        """Establece el valor del número de vecinos por la derecha"""
        self.Neighbours['R'] = v

    def getRightNeighbour (self):
        """Devuelve el número de vecinos por la derecha"""
        return self.Neighbours['R']

    def setLeftNeighbour (self, v):
        """Establece el valor del número de vecinos por la izquierda"""
        self.Neighbours['L'] = v

    def getLeftNeighbour (self):
        """Devuelve el número de vecinos por la izquierda"""
        return self.Neighbours['L']

    def setUpNeighbour (self, v):
        """Establece el valor del número de vecinos por la parte superior"""
        self.Neighbours['U'] = v

    def getUpNeighbour (self):
        """Devuelve el número de vecinos por la parte superior"""
        return self.Neighbours['U']

    def setDownNeighbour (self, v):
        """Establece el valor del número de vecinos por la parte inferior"""
        self.Neighbours['D'] = v

    def getDownNeighbour (self):
        """Devuelve el número de vecinos por la parte inferior"""
        return self.Neighbours['D']

    def getUpIbs (self):
        """Devuelve el valor de la parte superior a interpolar"""
        return max(self.getY1() - self.getIbs(), 0)

    def getDownIbs (self):
        """Devuelve el valor de la parte inferior a interpolar"""
        return min(self.getY2() + self.getIbs(), self.getResY())

    def getLeftIbs (self):
        """Devuelve el valor de la parte izquierda a interpolar"""
        return max(self.getX1() - self.getIbs(), 0)

    def getRightIbs (self):
        """Devuelve el valor de la parte derecha a interpolar"""
        return min(self.getX2() + self.getIbs(), self.getResX())

    def isRightNeighbour (self, p):
        """Indica si p es vecino derecho, y devuelve el rango de vecindad en su caso"""

        if self.getX2() == p.getX1() and (self.getY1() == p.getY1() or self.getY2() == p.getY2() or (self.getY1() < p.getY1() and self.getY2() > p.getY2()) or (self.getY1() > p.getY1() and self.getY2() < p.getY2())):
            if self.getYSize() > p.getYSize():
                return True, (p.getX1(), p.getY1(), p.getX1(), p.getY2())
            else:
                return True, (self.getX2(), self.getY1(), self.getX2(), self.getY2())
        else:
            return False, None

    def isLeftNeighbour (self, p):
        """Indica si p es vecino izquierdo, y devuelve el rango de vecindad en su caso"""

        if self.getX1() == p.getX2() and (self.getY1() == p.getY1() or self.getY2() == p.getY2() or (self.getY1() < p.getY1() and self.getY2 > p.getY2()) or (self.getY1() > p.getY1() and self.getY2() < p.getY2())):
            if self.getYSize() > p.getYSize():
                return True, (p.getX2(), p.getY1(), p.getX2(), p.getY2())
            else:
                return True, (self.getX1(), self.getY1(), self.getX1(), self.getY2())
        else:
            return False, None

    def isDownNeighbour (self, p):
        """Indica si p es vecino inferior, y devuelve el rango de vecindad en su caso"""

        if self.getY2() == p.getY1() and (self.getX1() == p.getX1() or self.getX2() == p.getX2() or (self.getX1() < p.getX1() and self.getX2() > p.getX2()) or (self.getX1() > p.getX1() and self.getX2() < p.getX2())):
            if self.getXSize() > p.getXSize():
                return True, (p.getX1(), p.getY1(), p.getX2(), p.getY1())
            else:
                return True, (self.getX1(), self.getY2(), self.getX2(), self.getY2())
        else:
            return False, None

    def isUpNeighbour (self, p):
        """Indica si p es vecino superior, y devuelve el rango de vecindad en su caso"""

        if self.getY1() == p.getY2() and (self.getX1() == p.getX1() or self.getX2() == p.getX2() or (self.getX1() < p.getX1() and self.getX2() > p.getX2()) or (self.getX1() > p.getX1() and self.getX2() < p.getX2())):
            if self.getXSize() > p.getXSize():
                return True, (p.getX1(), p.getY2(), p.getX2(), p.getY2())
            else:
                return True, (self.getX1(), self.getY1(), self.getX2(), self.getY1())
        else:
            return False, None
        
    def __eq__ (self, p):
        """Indica si dos objetos son iguales"""

        if self.getX1() == p.getX1() and self.getX2() == p.getX2() and self.getY1() == p.getY1() and self.getY2() == p.getY2():
            return True
        else:
            return False

    def __str__ (self):
        """Devuelve una cadena que representa el trozo de imagen"""
        return '[' + str(self.getX1()) + ', ' + str(self.getY1()) + ', ' + str(self.getX2()) + ', ' + str(self.getY2()) + '] Ibs: ' + str(self.getIbs())

class ImageSet:
    """La clase ImageSet representa funcionalidad asociada al tratamiento de la información que representan los trozos de imagen"""

    def __init__ (self):
        """Crea un objeto de tipo ImageLibrary"""
        self.Images = {}

    def add (self, id, pieceOfImage):
        """Añade una nueva representación de un trozo de la imagen"""
        self.Images[id] = pieceOfImage

    def getImages (self):
        """Devuelve el conjunto de trozos de imagen"""
        return self.Images

    def getImage (self, i):
        """Devuelve el trozo de la imagen identificado por i"""
        return self.getImages.get(i)

    def setNeighbourhood (self, piece):
        """Establece el número de vecinos de piece por cada lado"""

        r, l, u, d = 0, 0, 0, 0

        for p in self.getImages().values():

            if piece != p:
                # Vecinos por la derecha.
                if piece.getX2() == p.getX1() and (piece.getY1() == p.getY1() or piece.getY2() == p.getY2() or (piece.getY1() < p.getY1() and piece.getY2() > p.getY2()) or (piece.getY1() > p.getY1() and piece.getY2() < p.getY2())):
                    r += 1
                # Vecinos por la izquierda.
                if piece.getX1() == p.getX2() and (piece.getY1() == p.getY1() or piece.getY2() == p.getY2() or (piece.getY1() < p.getY1() and piece.getY2() > p.getY2()) or (piece.getY1() > p.getY1() and piece.getY2() < p.getY2())):
                    l += 1
                # Vecinos por la parte superior.
                if piece.getY1() == p.getY2() and (piece.getX1() == p.getX1() or piece.getX2() == p.getX2() or (piece.getX1() < p.getX1() and piece.getX2() > p.getX2()) or (piece.getX1() > p.getX1() and piece.getX2() < p.getX2())):
                    u += 1
                # Vecinos por la parte inferior.
                if piece.getY2() == p.getY1() and (piece.getX1() == p.getX1() or piece.getX2() == p.getX2() or (piece.getX1() < p.getX1() and piece.getX2() > p.getX2()) or (piece.getX1() > p.getX1() and piece.getX2() < p.getX2())):
                    d += 1

        piece.setRightNeighbour(r)
        piece.setLeftNeighbour(l)
        piece.setUpNeighbour(u)
        piece.setDownNeighbour(d)
