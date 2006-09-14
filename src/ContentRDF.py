#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern�ndez ************************#
#************************************************************#

import xml.dom.minidom
from xml.dom.ext.c14n import Canonicalize

def createAction (act, actor, arguments):

    action = xml.dom.minidom.Document()

    # RDF es la raíz del mensaje.
    rootElem = action.createElement('RDF')
    action.appendChild(rootElem)

    # Atributos de RDF.
    rootElem.setAttribute('xmlnsrdf', 'http://www.w3.org/1999/02/22-rdf-syntax.ns')
    rootElem.setAttribute('xmlnsfipa', 'http://www.fipa.org/schemas/fipa-rdf0#')

    # Acción.
    actionElem = action.createElement('Action')
    rootElem.appendChild(actionElem)
    actionElem.setAttribute('id', actor + 'Action')

    # Actor.
    actorElem = action.createElement('Actor')
    actionElem.appendChild(actorElem)
    actorText = action.createTextNode(actor)
    actorElem.appendChild(actorText)

    # Act.
    actElem = action.createElement('Act')
    actionElem.appendChild(actElem)
    actText = action.createTextNode(act)
    actElem.appendChild(actText)

    # Arguments.
    argumentsElem = action.createElement('Argument')
    actionElem.appendChild(argumentsElem)
    bagElem = action.createElement('Bag')
    argumentsElem.appendChild(bagElem)

    # Lista de argumentos.
    for x in arguments:
        argumentElem = action.createElement('Li')
        bagElem.appendChild(argumentElem)
        argumentText = action.createTextNode(x)
        argumentElem.appendChild(argumentText)

    print action.toprettyxml()

    return 0, Canonicalize(action)

def createProposition (subject, predicate, object):

    action = xml.dom.minidom.Document()

    # RDF es la raíz del mensaje.
    rootElem = action.createElement('RDF')
    action.appendChild(rootElem)

    # Atributos de RDF.
    rootElem.setAttribute('xmlnsrdf', 'http://www.w3.org/1999/02/22-rdf-syntax.ns')
    rootElem.setAttribute('xmlnsfipa', 'http://www.fipa.org/schemas/fipa-rdf0#')

    descElem = action.createElement('rdfDescription')
    rootElem.appendChild(descElem)
    descElem.setAttribute('ID', subject)

    # Predicate
    predicateElem = action.createElement(predicate)
    descElem.appendChild(predicateElem)
    predicateText = action.createTextNode(object)
    predicateElem.appendChild(predicateText)

    print action.toprettyxml()

    return 0, Canonicalize(action)
