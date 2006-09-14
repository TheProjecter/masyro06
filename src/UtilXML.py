#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fern醤dez ************************#
#************************************************************#

import xml.dom.minidom
from xml.dom.minidom import parse, parseString
import Ice
Ice.loadSlice('../FIPA/FIPA.ice', ['-I' '/usr/share/slice'])
import FIPA

def getAttribute (node, attribute):
    """Devuelve el valor del atributo attribute en relaci贸n al elemento node"""
    return str(node.getAttribute(attribute))

def initAgent (file):
    """Obtiene AgentIdentifier y AgentDescription a partir de la especificaci贸n en XML de file"""
    
    addresses = []

    try:
        doc = parse(file)
    except IOError:
        raise IOError
        
    root = doc.firstChild

    # Se obtiene el nombre del agente.
    name = str(getName(root)) + '@MASYRO'

    # Se obtiene la lista de direcciones del agente y su descripci贸n en el Directory Facilitator.
    for x in root.childNodes:
        if x.nodeType == x.ELEMENT_NODE and x.nodeName == 'address':
            addresses.append(str(getAddress(x)))
        elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'agentDescription':
            agentDescription = getAgentDescription(name, addresses, x)

    return FIPA.TAID(name, addresses), agentDescription

def getName (root):
    """Devuelve una cadena con el nombre del agente"""
    return root.getAttribute('name')

def getAddress (address):
    """Devuelve una cadena con la direcci贸n del agente"""
    return address.getAttribute('dir')

def getAgentDescription (name, addresses, ad):
    """Devuelve un objeto de tipo TDFAgentDescription a partir de ad"""

    services, protocols, ontologies, languages, scope = [], [], [], [], []
    leaseTime = 86400

    for x in ad.childNodes:
        # Se obtiene el servicio del agente.
        if x.nodeType == x.ELEMENT_NODE and x.nodeName == 'service':
            sde = FIPA.TDFServiceDescription(getAttribute(x, 'name'), getAttribute(x, 'type'))
            services.append(sde)
        # Se obtiene el protocolo del agente.
        elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'protocol':
            protocols.append(getAttribute(x, 'value'))
        # Se obtiene la ontolog铆a del agente.
        elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'ontology':
            ontologies.append(getAttribute(x, 'value'))
        # Se obtiene el lenguage del agente.
        elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'language':
            languages.append(getAttribute(x, 'value'))
        # Se obtiene el leaseTime del agente.
        elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'leaseTime':
            leaseTime = int(getAttribute(x, 'value'))
        # Se obtiene el scope del agente.
        elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'scope':
            scope.append(getAttribute(x, 'value'))

    aid = FIPA.TAID(name, addresses)
    return FIPA.TDFAgentDescription(aid, services, protocols, ontologies, languages, leaseTime, scope)

def readACLMessage (node):
    """Obtiene act, sender, addressesSender, receivers, addressesReceivers, content, language, protocol, conversation-id de node"""

    root = node.firstChild
    # Se obtiene el tipo de acto comunicativo.
    act = getAttribute(root, 'act')
        
    if root.nodeType == root.ELEMENT_NODE and root.nodeName == 'fipa-message':
        for x in root.childNodes:
            # Se obtiene el emisor del mensaje.
            if x.nodeType == x.ELEMENT_NODE and x.nodeName == 'sender':
                sender, addressesSender = getSender(x)
            # Se obtienen los receptores del mensaje.
            elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'receiver':
                receivers, addressesReceivers = getReceiver(x)
            # Se obtiene el contenido del mensaje.
            elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'content':
                content = getContent(x)
            # Se obtiene el tipo del lenguaje asociado al contenido del mensaje.
            elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'language':
                language = getLanguage(x)
            # Se obtiene el protocolo utilizado en el mensaje.
            elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'protocol':
                protocol = getProtocol(x)
            # Se obtiene el identificador de conversaci贸n asociado al mensaje.
            elif x.nodeType == x.ELEMENT_NODE and x.nodeName == 'conversation-id':
                idConv = getIdConv(x)

    return act, sender, addressesSender, receivers, addressesReceivers, content, language, protocol, idConv

def getSender (sender):
    """Devuelve una cadena con el nombre del emisor y una lista con sus direcciones de contacto"""

    name = sender.firstChild.firstChild.getAttribute('id')
    addresses = []
        
    for x in sender.firstChild.childNodes[1].childNodes:
        addresses.append(x.getAttribute('href'))

    return name, addresses

def getReceiver (receiver):
    """Devuelve una lista con los nombres de los receptores y otra lista con sus direcciones de contacto correspondientes"""

    names, addresses = [], []

    for x in receiver.childNodes:
        names.append(x.firstChild.getAttribute('id'))
        aux = []
        for y in x.childNodes[1].childNodes:
            aux.append(y.getAttribute('href'))
        addresses.append(aux)

    return names, addresses

def getContent (content):
    """Devuelve una cadena con el contenido del mensaje"""
    return content.firstChild.nodeValue

def getLanguage (language):
    """Devuelve una cadena con el lenguaje asociado al contenido del mensaje"""
    return language.firstChild.nodeValue

def getProtocol (protocol):
    """Devuelve una cadena con el protocolo empleado en el mensaje"""
    return protocol.firstChild.nodeValue

def getIdConv (idConv):
    """Devuelve una cadena con el id de la conversaci贸n"""
    return idConv.firstChild.nodeValue
