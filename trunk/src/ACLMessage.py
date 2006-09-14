#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fernández ************************#
#************************************************************#

import Ice
Ice.loadSlice('../FIPA/FIPA.ice', ['-I' '/usr/share/slice'])
import FIPA
import xml.dom.minidom
from xml.dom.ext.c14n import Canonicalize

class ACLMessage:

    def __init__ (self):
        print 'Sin parámetros'

    def __init__ (self, performative, to, _from, aclRepresentation, language, content, protocol, idConv):

        self.Performative = performative
        self.To = to
        self.From = _from
        self.ACLRepresentation = aclRepresentation
        self.Language = language
        self.Content = content
        self.Protocol = protocol
        self.IdConv = idConv

    def getPerformative (self):
        return self.Performative

    def getTo (self):
        return self.To

    def getFrom (self):
        return self.From

    def getACLRepresentation (self):
        return self.ACLRepresentation

    def getLanguage (self):
        return self.Language

    def getContent (self):
        return self.Content

    def getProtocol (self):
        return self.Protocol

    def getIDConv (self):
        return self.IdConv

    def createFIPAACLMessage (self):

        if self.getACLRepresentation() == FIPA.EAclRepresentation.bitefficientRep:
            return self.createFIPAACLMessageBitEfficient()
        elif self.getACLRepresentation() == FIPA.EAclRepresentation.stringRep:
            return self.createFIPAACLMessageString()
        elif self.getACLRepresentation() == FIPA.EAclRepresentation.xmlRep:
            return self.createFIPAACLMessageXML()
        else:
            return -1, ''

    def createFIPAACLMessageBitEfficient (self):
        # PENDIENTE
        return 0, ''

    def createFIPAACLMessageString (self):
        # PENDIENTE
        return 0, ''

    def createFIPAACLMessageXML (self):

        aclMessage = xml.dom.minidom.Document()

        # fipa-message es la raíz del mensaje.
        rootElem = aclMessage.createElement('fipa-message')

        # Tipo del mensaje.
        rootElem.setAttribute('act', self.getPerformative())
        aclMessage.appendChild(rootElem)

        # Emisor del mensaje.
        senderElem = aclMessage.createElement('sender')
        rootElem.appendChild(senderElem)
        agentIdentifierElem = aclMessage.createElement('agent-identifier')
        senderElem.appendChild(agentIdentifierElem)

        # Nombre del agente emisor del mensaje.
        nameElem = aclMessage.createElement('name')
        agentIdentifierElem.appendChild(nameElem)
        nameElem.setAttribute('id', self.getFrom().Name)

        # Dirección/es del agente emisor del mensaje.
        addressesElem = aclMessage.createElement('addresses')
        agentIdentifierElem.appendChild(addressesElem)

        for i in range(len(self.getFrom().Addresses)):
            urlElem = aclMessage.createElement('url')
            addressesElem.appendChild(urlElem)
            urlElem.setAttribute('href', self.getFrom().Addresses[i])

        # Receptor/es del mensaje
        receiverElem = aclMessage.createElement('receiver')
        rootElem.appendChild(receiverElem)

        # Nombre/s y dirección/es del agente o agentes receptor/es.
        for i in range(len(self.getTo())):
            agentIdentifierElem = aclMessage.createElement('agent-identifier')
            receiverElem.appendChild(agentIdentifierElem)
            # Nombre.
            nameElem = aclMessage.createElement('name')
            agentIdentifierElem.appendChild(nameElem)
            nameElem.setAttribute('id', self.getTo()[i].Name)
            addressesElem = aclMessage.createElement('addresses')
            agentIdentifierElem.appendChild(addressesElem)
            # Direcciones de contacto.
            for j in range(len(self.getTo()[i].Addresses)):
                urlElem = aclMessage.createElement('url')
                addressesElem.appendChild(urlElem)
                urlElem.setAttribute('href', self.getTo()[i].Addresses[j])

        # Contenido del mensaje.
        contentElem = aclMessage.createElement('content')
        rootElem.appendChild(contentElem)
        contentText = aclMessage.createTextNode(self.getContent())
        contentElem.appendChild(contentText)

        # Lenguage del mensaje.
        languageElem = aclMessage.createElement('language')
        rootElem.appendChild(languageElem)
        languageText = aclMessage.createTextNode(self.getLanguage())
        languageElem.appendChild(languageText)

        # Protocolo de comunicación del mensaje.
        protocolElem = aclMessage.createElement('protocol')
        rootElem.appendChild(protocolElem)
        protocolText = aclMessage.createTextNode(self.getProtocol())
        protocolElem.appendChild(protocolText)

        # Identificador de la conversación asociada al mensaje.
        idConvElem = aclMessage.createElement('conversation-id')
        rootElem.appendChild(idConvElem)
        idConvText = aclMessage.createTextNode(self.getIDConv())
        idConvElem.appendChild(idConvText)

        return 0, Canonicalize(aclMessage)
