#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern�ndez ************************#
#************************************************************#

class Zone:
    """La clase Zone representa una zona dentro de la división en zonas de la imagen que representa al modelo"""

    def __init__ (self, id, x1, y1, x2, y2):
        """Crea un objeto de tipo Zone"""

        # Identificador de la zona.
        self.Id = id
        # Coordenadas de la zona.
        self.X1, self.Y1 = x1, y1
        self.X2, self.Y2 = x2, y2
        # Variables relativas a la desviación típica, y la media de cada zona.
        self.Desv, self.Med = float(0), float(0)

    def setId (self, id):
        """Establece el valor del identificador de la zona"""
        self.Id = id

    def getId (self):
        """Devuelve el valor del identificador de la zona"""
        return self.Id

    def setX1 (self, x1):
        """Establece el valor de la coordenada X1"""
        self.X1 = x1

    def getX1 (self):
        """Devuelve el valor de la coordenada X1"""
        return self.X1

    def setY1 (self, y1):
        """Establece el valor de la coordenada Y1"""
        self.Y1 = y1

    def getY1 (self):
        """Devuelve el valor de la coordenada Y1"""
        return self.Y1

    def setX2 (self, x2):
        """Establece el valor de la coordenada X2"""
        self.X2 = x2

    def getX2 (self):
        """Devuelve el valor de la coordenada X2"""
        return self.X2

    def setY2 (self, y2):
        """Establece el valor de la coordenada Y2"""
        self.Y2 = y2

    def getY2 (self):
        """Devuelve el valor de la coordenada Y2"""
        return self.Y2

    def setDesv (self, desv):
        """Establece el valor de la variable Desv"""
        self.Desv = float(desv)

    def getDesv (self):
        """Devuelve el valor de la variable Desv"""
        return self.Desv

    def setMed (self, med):
        """Establece el valor de la variable Med"""
        self.Med = float(med)

    def getMed (self):
        """Devuelve el valor de la variable Med"""
        return self.Med

    def getWidth (self):
        """Devuelve la anchura de la zona"""
        return self.getX2() - self.getX1()

    def getHeight (self):
        """Devuelve la altura de la zona"""
        return self.getY2() - self.getY1()

    def getSize (self):
        """Devuelve el tamaño de la zona"""
        return self.getWidth() * self.getHeight()

    def __eq__ (self, z):
        """Compara dos zonas"""

        if self.getId() == z.getId():
            return True
        else:
            return False

    def __str__ (self):
        """Devuelve una cadena que representa la zona"""
        return 'Id: ' + str(self.getId()) + ' [' + str(self.getX1()) + ', ' + str(self.getY1()) + ', ' + str(self.getX2()) + ', ' + str(self.getY2()) + ']' + ' Desv: ' + str(self.getDesv()) + ' Med: ' + str(self.getMed()) + ' Size: ' + str(self.getSize())
