#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fernández ************************#
#************************************************************#

import xml.dom.minidom
import xml.dom.ext
import Util

class Fuzzy:
    """La clase Fuzzy representa la funcionalidad asociada a un conjunto difuso"""

    def __init__ (self, a, b, c, d, k = 1.0):
        """Crea un objeto de tipo Fuzzy"""

        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)
        self.k = float(k)

    def domain (self):
        """Devuelve el dominio asociado al conjunto difuso"""

        a = min(self.a, self.b, self.c, self.d)
        b = max(self.a, self.b, self.c, self.d)
        return (a, b)

    def copy (self):
        """Devuelve una copia del objeto de tipo Fuzzy"""
        return Fuzzy(self.a, self.b, self.c, self.d)

    def eval (self, num):
        """Devuelve la evaluación de num en el conjunto difuso"""

        if num <= self.a:
            return 0.0
        elif (num > self.a) and (num < self.b) and (self.a <> self.b):
            return ((num - self.a) / (self.b - self.a)) * self.k
        elif (num >= self.b) and (num <= self.c):
            return self.k
        elif (num > self.c) and (num < self.d) and (self.d <> self.c):
            return ((self.d - num) / (self.d - self.c)) * self.k
        else:
            return 0.0

    def __call__ (self, num):
        """Devuelve la evaluación de num en el conjunto difuso"""
        return self.eval(num)

    def __str__ (self):
        """Devuelve una cadena que representa los valores de la gráfica de la función de pertenencia"""
        return '[' + str(self.a) + ',' + str(self.b) + ',' + str(self.c) + ',' + str(self.d) + ']'

    def changeK (self, k1):
        """Cambia el valor de creencia del elemento perfecto"""

        self.b = (self.b - self.a) * k1 / self.k + self.a
        self.c = self.d - (self.d - self.c) * k1 / self.k
        self.k = k1

    def area (self):
        """Devuelve el área encerrada bajo la función de pertenencia"""
        return float(((self.d - self.a) + (self.c - self.b)) * self.k / 2.0)

    def cg (self):
        """Devuelve el valor asociado al centro de gravedad del conjunto difuso"""

        S = self.area()
        if S == 0:
            return self.a
        else:
            # Baricentros
            b1 = (self.a + self.b * 2.0) / 3.0
            b2 = (self.b + self.c) / 2.0
            b3 = (self.c * 2.0 + self.d) / 3.0
            # �reas
            a1 = (self.b - self.a) * self.k / 2.0
            a2 = (self.c - self.b) * self.k
            a3 = (self.d - self.c) * self.k / 2.0
            return (a1 * b1 + a2 * b2 + a3 * b3) / S

class FuzzyVar:
    """La clase FuzzyVar representa una variable lingüística"""

    def __init__ (self, name):
        """Crea un objeto del tipo FuzzyVar"""

        self.name = name
        self.values = {}
        self.domain = None

    def setValue (self, label, value):
        """Añade una nueva partición definida por value a la variable lingüística"""

        if not self.values.has_key(label):
            self.values[label] = value
            if not (self.domain == None):
                a, b = value.domain()
                self.domain = (min(self.domain[0], a), max(self.domain[1], b))
            else:
                self.domain = value.domain()

    def getValue (self, label, num):
        """Devuelve el grado de pertenencia de num en la partición definida por label"""

        if not self.values.has_key(label):
            return 0.0
        else:
            return self.values[label](num)

    def __call__ (self, label, num):
        """Devuelve el grado de pertenencia de num en la partición definida por label"""
        return self.getValue(label, num)

    def allEval (self, num):
        """Devuelve el grado de pertenencia de num en todas las particiones establecidas"""

        res = {}
        for label in self.values.keys():
            res[label] = self.values[label](num)
        return res

    def allDesf (self):
        """Devuelve el centro de gravedad de todas las particiones establecidas"""

        res = {}
        for label in self.values.keys():
            res[label] = self.values[label].cg()
        return res

class FuzzySystem:
    """La clase FuzzySystem representa el sistema difuso"""

    def __init__ (self, name = 'NoName', tnorm = min, tconorm = max):
        """Crea un objeto de tipo FuzzySystem"""

        self.name = name
        self.rules = []
        self.var = {}
        self.resp = None
        self.tnorm = tnorm
        self.tconorm = tconorm

    def insertVar (self, var):
        """Añade una nueva variable al sistema difuso"""
        self.var[var.name] = var

    def insertRule (self, listAnt, listCons):
        """Añade una nueva regla al sistema difuso"""
        self.rules.append((listAnt, listCons))

    def strRule (self, rule):
        """Devuelve una cadena que representa la regla"""

        ListAnt, ListCons = rule
        straux = 'IF '
        for ant in ListAnt:
            straux = straux + str(ant[0]) + ' IS ' + str(ant[1]) + ' '
        straux = straux + ' THEN '
        for cons in ListCons:
            straux = straux + str(cons[0]) + ' IS ' + str(cons[1]) + ' '
        return straux

    def __str__ (self):
        """Devuelve una cadena que representa todas las reglas del sistema difuso"""

        straux = 'Rule System: ' + self.name + '\n'
        for i in range(0, len(self.rules)):
            straux = straux + '[' + str(i) + ']' + self.strRule(self.rules[i]) + '\n'
        return straux

    def setInput (self, ListInput):
        """Establece el valor de entrada de las variables"""

        self.resp = {}
        for input in ListInput:
            var, value = input
            self.resp[var] = self.var[var].allEval(value)
        return self.resp

    def evalAnt (self, rule):
        """Devuelve la tnorma relativa a los antecedentes de la regla"""

        listant, cons = rule
        seq = []
        for ant in listant:
            name, label = ant
            seq.append(self.resp[name][label])
        return self.tnorm(seq)

    def evalAll (self, ListInput):
        """Evalúa las entradas relativas a ListInput"""

        # res representa una lista con las tnormas de los antecedentes de cada una de las reglas.
        res = []
        # acu representa la suma de todos los elementos de res.
        acu = 0.0
        self.setInput(ListInput)
        # rescons representa los consecuentes de cada regla.
        rescons = {}
        for r in self.rules:
            listAnt, listCons = r
            ant = self.evalAnt(r)
            acu = acu + ant
            res.append(ant)
            if ant == 0.0:
                continue
            for cons in listCons:
                Var, Etiq = cons
                if not rescons.has_key(Var):
                    rescons[Var] = {Etiq:ant}
                elif not rescons[Var].has_key(Etiq):
                    rescons[Var][Etiq] = ant
                else:
                    rescons[Var][Etiq] = self.tconorm(rescons[Var][Etiq], ant)

        return res, acu, rescons

    def out (self, Listinput):
        """Devuelve la salida para cada una de las entradas definidas en Listinput"""

        a, a1, c = self.evalAll(Listinput)
        Resalida = {}
        for var in c.keys():
            sum, acu = 0.0, 0.0
            for etq in c[var]:
                new = self.var[var].values[etq]
                new = new.copy()
                new.changeK(c[var][etq])
                sum = sum + new.cg() * new.area()
                acu = acu + new.area()
                try:
                    res = sum / acu
                except ZeroDivisionError:
                    res = sum
            Resalida[var] = res
        return Resalida

class UtilFuzzy:
    """La clase UtilFuzzy representa la funcionalidad relativa al tratamiento del fichero en formato xml de entrada"""

    def __init__ (self):
        """Constructor de la clase UtilFuzzy"""

        self.SystemName = ''
        self.Variables = []
        self.Antecedents = []
        self.Consequences = []

    def setSystemName (self, systemName):
        """Establece el valor de la variable SystemName"""
        self.SystemName = systemName

    def getSystemName (self):
        """Devuelve el valor de la variable SystemName"""
        return self.SystemName

    def insertVariable (self, var):
        """Inserta una variable en la lista de variables"""
        self.Variables.append(var)

    def getVariables (self):
        """Devuelve la lista de variables"""
        return self.Variables

    def insertAntecedent (self, antecedent):
        """Inserta una lista con los antecedentes asociados a la regla i."""
        self.Antecedents.append(antecedent)

    def insertConsequence (self, consequence):
        """Inserta una lista con los consecuentes asociados a la regla i."""
        self.Consequences.append(consequence)

    def getAntecedents (self):
        """Devuelve los antecedentes de todas las reglas"""
        return self.Antecedents

    def getConsequences (self):
        """Devuelve los consecuentes de todas las reglas"""
        return self.Consequences

    def loadFile (self, file):
        """Carga el fichero de entrada e inicializa las variables Sistema, Variables, y Reglas"""

        doc = xml.dom.minidom.parse(file)
        system = doc.firstChild.childNodes[1]

        # Se establece el nombre del sistema.
        self.setSystemName(system.getAttribute('name'))

        # Se establecen las variables y las reglas del sistema.
        for x in system.childNodes:
            
            # Variable lingüística.
            if x.nodeType == x.ELEMENT_NODE and x.nodeName == 'linguisticvar':
                name, type = x.getAttribute('name'), x.getAttribute('type')
                var = FuzzyVar(name)
                
                # Se obtienen los conjuntos difusos de esa variable lingüística.
                for y in x.childNodes:
                    if y.nodeType == y.ELEMENT_NODE and y.nodeName == 'fuzzyset':
                        label = y.getAttribute('label')
                        a, b, c, d = y.getAttribute('a'), y.getAttribute('b'), y.getAttribute('c'), y.getAttribute('d')
                        var.setValue(label, Fuzzy(a, b, c, d))

                # Se inserta la variable en la lista de variables.
                self.insertVariable(var)

                var = None

            # Regla.
            elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'rule':
                ant, cons = [], []
                
                for y in x.childNodes:
                    if y.nodeType == y.ELEMENT_NODE and y.nodeName == 'antecedent':
                        ant.append((y.getAttribute('varname'), y.getAttribute('linguisticlabel')))
                    elif y.nodeType == y.ELEMENT_NODE and y.nodeName == 'consequence':
                        cons.append((y.getAttribute('varname'), y.getAttribute('linguisticlabel')))

                # Se insertan los antecedentes y consecuentes de la regla i.
                self.insertAntecedent(ant)
                self.insertConsequence(cons)

    def loadInputData (self, s, co, nd, file):
        """Inicializa las variables de entrada"""

        doc = xml.dom.minidom.parse(file)
        system = doc.firstChild.childNodes[1]

        # Se establecen las variables y las reglas del sistema.
        for x in system.childNodes:
            
            # Variable lingüística.
            if x.nodeType == x.ELEMENT_NODE and x.nodeName == 'linguisticvar':
                name, type = x.getAttribute('name'), x.getAttribute('type')
                var = FuzzyVar(name)

                # Tamaño del trozo.
                if name == 'S':
                    for y in x.childNodes:
                        if y.nodeType == y.ELEMENT_NODE and y.nodeName == 'fuzzyset':
                            label = y.getAttribute('label')
                            a, b, c, d = s[label][0], s[label][1], s[label][2], s[label][3]
                            y.setAttribute('a', a)
                            y.setAttribute('b', b)
                            y.setAttribute('c', c)
                            y.setAttribute('d', d)

                # Complejidad del trozo.
                elif name == 'C':
                    for y in x.childNodes:
                        if y.nodeType == y.ELEMENT_NODE and y.nodeName == 'fuzzyset':
                            label = y.getAttribute('label')
                            a, b, c, d = co[label][0], co[label][1], co[label][2], co[label][3]
                            y.setAttribute('a', a)
                            y.setAttribute('b', b)
                            y.setAttribute('c', c)
                            y.setAttribute('d', d)
                            #print 'COMPLEJIDAD: [' + str(y.getAttribute('a')) + ', ' + str(y.getAttribute('b')) + ', ' + str(y.getAttribute('c')) + ', ' + str(y.getAttribute('a')) +']'

                # Diferencia con los vecinos.
                elif name == 'Nd':
                    for y in x.childNodes:
                        if y.nodeType == y.ELEMENT_NODE and y.nodeName == 'fuzzyset':
                            label = y.getAttribute('label')
                            a, b, c, d = nd[label][0], nd[label][1], nd[label][2], nd[label][3]
                            y.setAttribute('a', a)
                            y.setAttribute('b', b)
                            y.setAttribute('c', c)
                            y.setAttribute('d', d)

        f = open(file, 'w')
        xml.dom.ext.PrettyPrint(doc, f)
        f.close()

if __name__ == '__main__':

    fuzzy = UtilFuzzy()
    fuzzy.loadFile('./prueba.xml')
    s, c, nd = Util.loadInput('./prueba.txt')
    fuzzy.loadInputData(s, c, nd, './prueba.xml')

    InputData = []
    InputData.append((('C', 8), ('S', 38400), ('Op', 15.0), ('Nd', 33)))
    
    System = FuzzySystem(fuzzy.getSystemName())
    
    # Variables del sistema.
    for x in fuzzy.getVariables():
        System.insertVar(x)

    print System.var.keys()
    print ''
    for x in System.var.values():
        print x.values.keys()
        for y in x.values.values():
            print y.a, y.b, y.c, y.d
        print ''

    # Reglas del sistema.
    for i in range(len(fuzzy.getAntecedents())):
        System.insertRule(fuzzy.getAntecedents()[i], fuzzy.getConsequences()[i])

    for x in InputData:
        a, b, c = System.evalAll(x)
        print a
        print b
        print c
        print System.out(x)
