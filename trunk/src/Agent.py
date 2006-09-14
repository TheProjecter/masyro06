#!/usr/bin/python
# -*- coding: utf-8 -*-

#************************************************************#
#**** MASYRO: A MultiAgent SYstem for Render Optimization ***#
#**** Autor: David Vallejo Fernández ************************#
#************************************************************#

import sys, time
import Ice, Glacier2
import xml.dom.minidom
from xml.dom.minidom import parseString
Ice.loadSlice('../FIPA/FIPA.ice', ['-I' '/usr/share/slice'])
import FIPA
import ACLMessage, ContentRDF
import Util, UtilXML

class AgentI (FIPA.Agent, Ice.Application):
    """La clase AgentI representa un agente genérico"""

    def __init__ (self):
        """Crea un objeto del tipo AgentI"""

        # Se obtiene el nombre del fichero en formato XML para inicializar el agente.
        inputFile = self.getArguments()
        if inputFile == '':
            print 'Sinopsis: python Agent.py -i <file.xml>'
            sys.exit(0)
            
        # AgentIdentifier representa la identificación del agente: name y addresses.
        # AgentDescription representa la descripción del agente en el Directory Facilitator.
        try:
            self.AgentIdentifier, self.AgentDescription = UtilXML.initAgent(inputFile)
        except IOError:
            print 'El archivo ' + inputFile + ' no existe. Sinopsis: python Agent.py -i <file>'
            sys.exit(0)
        
        # AgentDescriptions representa la lista de objetos que describen a otros agentes del Directory Facilitator.
        self.AgentDescriptions = []
        # State representa el estado del agente en la plataforma de agentes.
        self.State = FIPA.EState.Initiated

        # ServiceRoot representa la lista de servicios básicos de la plataforma.
        self.ServiceRoot = []
        # Proxies a los servicios básicos de la plataforma de agentes.
        self.StartService, self.Ams, self.Df, self.Acc = None, None, None, None

    def getArguments (self):
        """Devuelve los parámetros representativos a la hora de inicializar un agente"""

        inputFile = ''

        for i in range(1, len(sys.argv)):
            if sys.argv[i] == "-i":
                try:
                    inputFile = sys.argv[i + 1]
                except IndexError:
                    inputFile = ''

        return inputFile

    def getAgentIdentifier (self):
        """Devuelve el Agent Identifier Description asociado al agente"""
        return self.AgentIdentifier

    def setName (self, name):
        """Cambia el nombre del agente a name"""
        self.getAgentIdentifier().Name = name

    def getName (self):
        """Devuelve el nombre del agente"""
        return self.getAgentIdentifier().Name

    def addAddress (self, address):
        """Añade una dirección de contacto a la lista de direcciones del agente"""
        self.getAddresses().append(address)

    def removeAddress (self, address):
        """Elimina una dirección de contacto de la lista de direcciones del agente"""
        self.getAddresses().remove(address)

    def getAddresses (self):
        """Devuelve la lista de direcciones de contacto del agente"""
        return self.getAgentIdentifier().Addresses

    def getAgentDescription (self):
        """Devuelve la descripción del agente en el Directory Facilitator"""
        return self.AgentDescription

    def getServices (self):
        """Devuelve la lista con los servicios soportados por el agente"""
        return self.getAgentDescription().Services

    def addService (self, name, type):
        """Añade un servicio soportado por el agente"""
        self.getServices().append(FIPA.TDFServiceDescription(name, type))

    def getProtocols (self):
        """Devuelve la lista de protocolos de interacción soportados por el agente"""
        return self.getAgentDescription().Protocols

    def addProtocol (self, protocol):
        """Añade un protocolo de interacción a la lista de protocolos de interacción soportados por el agente"""
        self.getProtocols().append(protocol)

    def removeProtocol (self, protocol):
        """Elimina un protocolo de interacción de la lista de protocolos de interacción soportados por el agente"""
        self.getProtocols().remove(protocol)

    def getOntologies (self):
        """Devuelve la lista de ontologies conocidas por el agente"""
        return self.getAgentDescription().Ontologies

    def addOntology (self, ontology):
        """Añade una ontología a la lista de ontologías conocidas por el agente"""
        self.getOntologies().append(ontology)

    def removeOntology (self, ontology):
        """Elimina un ontología de la lista de ontologías conocidas por el agente"""
        self.getOntologies().remove(ontology)

    def getLanguages (self):
        """Devuelve la lista de lenguajes de contenido soportados por el agente"""
        return self.getAgentDescription().Languages

    def addLanguage (self, language):
        """Añade un lenguaje a la lista de lenguajes de contenido conocidos por el agente"""
        self.getLanguages().append(language)

    def removeLanguage (self, language):
        """Elimina un lenguaje de la lista de lenguajes de contenido conocidos por el agente"""
        self.getLanguages().remove(language)

    def setLeaseTime (self, leaseTime):
        """Cambia el valor de la duración del registro del agente en el Directory Facilitator al valor leaseTime"""
        self.getAgentDescription().LeaseTime = leaseTime

    def getLeaseTime (self):
        """Devuelve la duración del registro del agente en el Directory Facilitator"""
        return self.getAgentDescription().LeaseTime

    def getScope (self):
        """Devuelve la visibilidad de la descripción del agente en el Directory Facilitator"""
        return self.getAgentDescription().Scope

    def addScope (self, scope):
        """Añade una visibilidad a la lista de visibilidades de la descripción del agente en el Directory Facilitator"""
        self.getScope().append(scope)

    def removeScope (self, scope):
        """Elimina una visibilidad de la lista de visibilidades de la descripción del agente en el Directory Facilitator"""
        self.getScope().remove(scope)

    def getAgentDescriptions (self):
        """Devuelve la lista de las descripciones de los agentes registrados en el Directory Facilitator"""
        return self.AgentDescriptions

    def addAgentDescription (self, agentDescription):
        """Añade la descripción de un agente registrado en el Directory Facilitator a la lista de descripciones"""
        self.getAgentDescriptions().append(agentDescription)

    def removeAgentDescription (self, agentDescription):
        """Elimina la descripción de un agente registrado en el Directory Facilitator de la lista de descripciones"""
        self.getAgentDescriptions().remove(agentDescription)

    def modifyAgentDescription (self, agentDescription):
        """Modifica la descripción de un agente registrado en el Directory Facilitator en la lista de descripciones"""
        
        for i in range(len(self.getAgentDescriptions())):
            if self.getAgentDescriptions()[i].Name.Name == agentDescription.Name.Name:
                self.getAgentDescriptions()[i] = agentDescription
                return True
        return False

    def setState (self, state):
        """Cambia el estado del agente al valor definido por state"""
        self.State = state

    def getState (self):
        """Devuelve el estado actual del agente"""
        return self.State

    def suspend (self, current = None):
        """Cambia el estado de un agente a Suspended"""
        self.setState(FIPA.EState.Suspended)

    def terminate (self, current = None):
        """Termina la ejecución de un agente"""
        self.deregister()

    def resume (self, current = None):
        """Cambia el estado del agente a activo"""
        self.setState(FIPA.EState.Resume)

    def send (self, performative, to, ACLRepresentation, payload, language, protocol, idConv):
        """Envía un mensaje ACL al Agent Communication Channel de la plataforma de agentes"""

        date = FIPA.TDate()
        envelope = FIPA.TEnvelope(to, self.AgentIdentifier, date, ACLRepresentation.value)
        aclMessage = ACLMessage.ACLMessage(performative, to, self.AgentIdentifier, ACLRepresentation, language, payload, protocol, idConv)

        errorCode, out = aclMessage.createFIPAACLMessage()

        print out

        message = FIPA.TMessage(envelope, out)

        self.sendAcc(message)

    def sendAcc (self, message):
        """Ejecutiva la funcionalidad remota del envío de un mensaje"""

        try:
            self.Acc.receive(message)
        except Ice.LocalException, message:
            print self.getName + ' --> Fue incapaz de enviar el mensaje.', message
            # PENDIENTE --> Decidir cómo actuar ante un fallo al enviar un mensaje.

    def receiveACLMessage (self, ACLMessage, current = None):
        """Recibe un mensaje ACL del Agent Communication Channel de la plataforma de agentes"""

        print self.getName() + ' --> Mensaje recibido.'

        try:
            # Conversión de string a Document.
            aclMessage = parseString(ACLMessage)
            print aclMessage.toprettyxml()
            # Lectura del documento XML.
            UtilXML.readACLMessage(aclMessage)
        except Exception, message:
            print 'Error al procesar el mensaje recibido: ', sys.exc_info()[0], message
            # PENDIENTE --> Decidir cómo actuar ante un fallo en la recepción del mensaje.

    def setServiceRoot (self, serviceRoot):
        """Establece el valor de la lista de servicios básicos"""
        self.ServiceRoot = serviceRoot

    def getServiceRoot (self):
        """Devuelve la lista de los servicios básicos de la plataforma"""
        return self.ServiceRoot

    def setStartService (self, startService):
        """Establece el proxy asociado al servicio Start Service"""
        self.StartService = startService

    def getStartService (self):
        """Devuelve el proxy asociado al servicio Start Service"""
        return self.StartService

    def obtainServiceRoot (self):
        """Obtiene los servicios básicos de la plataforma de agentes: AMS, Directory Facilitator, y ACC"""

        try:
            obj = self.communicator().stringToProxy('startService')
            self.setStartService(FIPA.StartServicePrx.checkedCast(obj))
            
        except Ice.NotRegisteredException:
            proxy = self.communicator().getProperties().getProperty('IceGrid.InstanceName') + '/Query'
            query = IceGrid.QueryPrx.checkedCast(self.communicator().stringToProxy(proxy))
            self.StartService = FIPA.StartServicePrx.checkedCast(query.findObjectByType('::FIPA::StartService'))

        except Ice.LocalException:
            print self.getName() + ' --> No pudo obtener los servicios b�sicos.'
            sys.exit(1)

        if not self.getStartService():
            print self.getName() + ' --> No pudo obtener los servicios b�sicos.'
            sys.exit(1)

        self.setServiceRoot(self.getStartService().getServiceRoot())

    def setContactAddress (self):
        """Establece la dirección de contacto del agente"""

        try:
            adapter = self.communicator().createObjectAdapterWithEndpoints(self.getName()+'Adapter', 'tcp')
            ident = Ice.stringToIdentity(self.getName())
            obj = adapter.add(self, ident)
            self.addAddress(self.communicator().proxyToString(obj))
            adapter.activate();

        except Ice.LocalException:
            print self.getName() + ' --> Error al establecer la dirección de contacto.'
            # PENDIENTE --> Decidir cómo actuar al no poder establecer dicha dirección.

        return adapter

    def getBasicServices (self):
        """Obtiene las referencias a los servicios básicos de la plataforma"""

        for service in self.getServiceRoot():
            if service.ServiceType == '::FIPA::AMS':
                self.getBasicServiceAMS(service)
            if service.ServiceType == '::FIPA::DirectoryFacilitator':
                self.getBasicServiceDF(service)
            if service.ServiceType == '::FIPA::ACC':
                self.getBasicServiceACC(service)

    def setAms (self, ams):
        """Establece el proxy al servicio Agent Management System"""
        self.Ams = ams

    def getAms (self):
        """Devuelve el proxy asociado al servicio Agent Management System"""
        return self.Ams

    def getBasicServiceAMS (self, service):
        """Obtiene la referencia al servicio AMS (Agent Management System) y registra al agente en el mismo"""

        explanation = FIPA.EExplanation.Invalid.value

        try:
            self.setAms(FIPA.AMSPrx.checkedCast(self.communicator().stringToProxy(service.ServiceLocator[0].ServiceAddress)))
        except Ice.LocalException:
            print self.getName() + ' --> Error al obtener un proxy al servicio AMS.'
            # PENDIENTE --> Decidir cómo actuar al no poder obtener un proxy al servicio AMS.
            
        print self.getName() + ' --> He obtenido una referencia al AMS.'

        # El agente se registra en la plataforma de agentes a través del AMS.
        explanation, state = self._cpp_register()
        self.setState(state)

        # Se comprueba si ha habido éxito en el registro.
        if explanation == FIPA.EExplanation.Success.value:
            print self.getName() + ' --> Registrado en la plataforma.'
        else:
            print self.getName() + ' --> Fue incapaz de registrarse en la plataforma.'

        print self.getName() + ' --> Mi estado es ', Util.traduceState(self.getState())

    def setDf (self, df):
        """Establece el proxy al servicio Directory Facilitator"""
        self.Df = df

    def getDf (self):
        """Devuelve el proxy asociado al servicio Directory Facilitator"""
        return self.Df

    def getBasicServiceDF (self, service):
        """Obtiene la referencia al servicio Directory Facilitator"""
        
        try:
            self.setDf(FIPA.DirectoryFacilitatorPrx.checkedCast(self.communicator().stringToProxy(service.ServiceLocator[0].ServiceAddress)))
        except Ice.LocalException:
            print self.getName() + ' --> Error al obtener un proxy al servicio Directory Facilitator.'
            # PENDIENTE --> Decidir cómo actuar al no poder obtener un proxy al servicio Directory Facilitator.
            
        print self.getName() + ' --> He obtenido una referencia al Directory Facilitator.'

    def setAcc (self, acc):
        """Establece el proxy al servicio Agent Communication Channel"""
        self.Acc = acc

    def getAcc (self):
        """Devuelve el proxy asociado al servicio Agent Communication Channel"""
        return self.Acc

    def getBasicServiceACC (self, service):
        """Obtiene la referencia al servico Agent Communication Channel"""

        try:
            self.setAcc(FIPA.ACCPrx.checkedCast(self.communicator().stringToProxy(service.ServiceLocator[0].ServiceAddress)))
        except Ice.LocalException:
            print self.getName() + ' --> Error al obtener un proxy al servicio Agent Communication Channel.'
            # PENDIENTE --> Decidir cómo actuar al no poder obtener un proxy al servicio Agent Communication Channel.
            
        print self.getName() + ' --> He obtenido una referencia al ACC.'        

    def _cpp_register (self):
        """Registra al agente en el AMS"""

        newName = ''

        try:
            explanation, newName, state = self.getAms().register(self.getAgentIdentifier())
            # Se comprueba el valor de explanation.
            # Ya existe un agente con ese nombre en la plataforma.
            if explanation == FIPA.EExplanation.Duplicate.value:
                # El AMS se encarga de asignar un nombre, previa solicitación del agente.
                self.setName('unknown')
                explanation, newName, state = self.getAms().register(self.AgentIdentifier)
                print self.getName() + ' --> Ya existe un agente con este nombre.'
                self.setName(newName)
                print self.getName() + ' --> Este es mi nuevo nombre: ' + self.getName()
            # El agente no está autorizado a realizar el registro.
            # PENDIENTE
            elif explanation == FIPA.EExplanation.Success.value:
                print self.getName() + ' --> Registro satisfactorio.'
            # El AID no es válido.
            elif explanation == FIPA.EExplanation.Invalid.value:
                # El AMS se encarga de asignar un nombre, previa solicitación del agente.
                self.setName('unknown')
                explanation, newName, state = self.getAms().register(self.getAgentIdentifier())
                self.setName(newName)
                self.setNameAgentDescription(newName)

        except Ice.LocalException, message:
            print self.getName() + ' --> Fue incapaz de registrarse.', message
            # PEDIENTE --> Decidir cómo actuar ante este fallo.

        return explanation, state

    # PENDIENTE --> definir un mensaje para el registro del agente.
    def FIPA_cpp_register (self):

        # Se crea el contenido del mensaje.
        errorCode, action = ContentRDF.createAction('register', self.getName(), [])

        # Si no hay ningún error se crea el mensaje ACL.
        if not errorCode:
            to = []
            aid = FIPA.TAID('ams', ['ams'])
            to.append(aid)
            self.send('request', to, FIPA.EAclRepresentation.xmlRep, action, 'fipa-rdf0', '', '1')

    def deregister (self):
        """Elimina el registro del agente en el AMS"""

        try:
            explanation = self.getAms().deregister(self.getAgentIdentifier())
        except Ice.LocalException, message:
            print self.getName() + ' --> Fue incapaz de darse de baja en el AMS.', message
            # PENDIENTE

    def subscribeDF (self):
        """Subscribe al agente dentro del servicio Directory Facilitator"""

        # El agente se subscribe al servicio Directory Facilitator.
        explanation = self.getDf().register(self.getAgentDescription())
        
        # Se comprueba si ha habido éxito en el registro con el Directory Facilitator.
        if explanation == FIPA.EExplanation.Success.value:
            print self.getName() + ' --> Registrado en el Directory Facilitator.'
        else:
            print self.getName() + ' --> No se pudo registrar en el Directory Facilitator.'

    def unsubscribeDF (self):
        """Elimina la subscripción del agente en el Directory Facilitator"""

        try:
            # El agente elimina su registro del servicio Directory Facilitator.
            explanation = self.getDf().deregister(self.getAgentDescription())
            # Se comprueba si ha habido éxito en la eliminación del registro con el Directory Facilitator.
            if explanation == FIPA.EExplanation.Success.value:
                print self.getName() + ' --> Dado de baja en el Directory Facilitator.'
            else:
                print self.getName() + ' --> No se pudo dar de baja en el Directory Facilitator'
        except Ice.LocalException, message:
            print self.getName() + ' --> Error al eliminar el registro en el Directory Facilitator.', sys.exc_info()[0], message
            # PENDIENTE

    def run (self, args):
        """Ejecución del código asociado al agente"""
                
        self.shutdownOnInterrupt()

        # Conexión con Glacier2.
        router = Glacier2.RouterPrx.checkedCast(self.communicator().getDefaultRouter())
        session = router.createSession('david', 'david')
        
        self.obtainServiceRoot()
        self.setContactAddress()
        self.getBasicServices()

        # Subscripción al Directory Facilitator.
        self.subscribeDF()

        #self.addProtocol('fipa-subscribe')
        #self.getDf().modify(self.getAgentDescription())
        #to = []
        #aid = FIPA.TAID('Mulder', ['Mulder:default -p 10005'])
        #to.append(self.getAgentIdentifier())
        #self.send('request', to, FIPA.EAclRepresentation.xmlRep, 'Este es el contenido.', 'PorDefinir', 'PorDefinir', '666')
        
	self.communicator().waitForShutdown()
        # Baja del Directory Facilitator y del AMS.
        self.deregister()
        self.unsubscribeDF()
	return 0
