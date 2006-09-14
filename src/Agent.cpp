/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <Agent.h>

// MÉTODO AgentI :: AgentI
AgentI::
AgentI(string name)
{

  AgentIdentifier.Name = name;

  AgentDescription.Name = AgentIdentifier;
  AgentDescription.Protocols.push_back("Ice");
  AgentDescription.Ontologies.push_back("");
  AgentDescription.Languages.push_back("");
  AgentDescription.LeaseTime = 86400;
  AgentDescription.Scope.push_back("MASYRO");

  this->setState(Initiated);

}
// FIN MÉTODO AgentI :: AgentI

// MÉTODO AgentI :: ~AgentI
AgentI::
~AgentI()
{

  int explanation = -1;

  //this->deregister(explanation);

}
// FIN MÉTODO AgentI :: ~AgentI

// METODO AgentI :: getServiceRoot
TServiceDirectoryEntries
AgentI::
getServiceRoot() const
{

  try
    {
      return startService->getServiceRoot();
    }// Fin try

  catch (const Ice::Exception& ex)
    {
      cerr << ex << endl;
    }// Fin catch

}
// FIN METODO AgentI :: getServiceRoot

// MÉTODO AgentI :: suspend
void
AgentI::
suspend(const ::Ice::Current&)
{

  // PENDIENTE
  this->setState(Suspended);
  cout << this->getName() << " --> Pasa a estado Suspended." << endl;

}
// FIN MÉTODO AgentI :: suspend

// MÉTODO AgentI :: terminate
void
AgentI::
terminate(const ::Ice::Current&)
{

  int explanation;

  try
    {
      explanation = -1;
      cout << this->getName() << " --> Finalizando su ejecución." << endl;
      // El agente se da de baja en la plataforma de agentes.
      this->deregister(explanation);
      communicator()->destroy();
      exit(0);
    }// Fin try
  catch (const Ice::Exception& ex)
    {
      cerr << ex << endl;
    }// Fin catch

}
// FIN MÉTODO AgentI :: terminate

// MÉTODO AgentI :: resume
void
AgentI::
resume(const ::Ice::Current&)
{

  // PENDIENTE
  this->setState(Active);
  cout << this->getName() << " --> Pasa a estado Active." << endl;

}
// FIN MÉTODO AgentI :: resume

// MÉTODO AgentI :: notify
void
AgentI::
notify(const ::FIPA::TDFAgentDescription& ad, ::Ice::Int operation, const ::Ice::Current&)
{

  switch (operation) {

    // Notificación del registro de un agente en el DirectoryFacilitator.
  case REGISTER:
    cout << this->getName() << " --> Ha llegado un nuevo evento del DirectoryFacilitator del tipo REGISTER." << endl;
    AgentDescriptions.push_back(ad);
    cout << this->getName() << " --> El agente " << ad.Name.Name << " se ha registrado como proveedor se servicios." << endl;
    break;
    
    // Notificación de la eliminación del registro de un agente en el DirectoryFacilitator.
  case DEREGISTER:
    cout << this->getName() << " --> Ha llegado un nuevo evento del DirectoryFacilitator del tipo DEREGISTER." << endl;
    // Se comprueba si el agente estaba en la lista de agentes conocidos.
    if (!Util::removeRegisteredAgentDF(ad.Name.Name, AgentDescriptions))
      cout << this->getName() << " --> El agente " << ad.Name.Name << " no estaba registrado." << endl;
    else
      cout << this->getName() << " --> El agente " << ad.Name.Name << " se ha dado de baja." << endl;
    break;

    // Notificación de la modificación del registro de un agente en el DirectoryFacilitator.
  case MODIFY:
    cout << this->getName() << " --> Ha llegado un nuevo evento del DirectoryFacilitator del tipo MODIFY." << endl;
    // Se comprueba si el agente estaba en la lista de agentes conocidos.
    if (!Util::modifyRegisteredAgentDF(ad, AgentDescriptions))
      cout << this->getName() << " --> El agente " << ad.Name.Name << " no estaba registrado en MASYRO." << endl;
    else
      cout << this->getName() << " --> El agente " << ad.Name.Name << " ha modificado su registro en MASYRO." << endl;
    break;

  }// Fin switch

}
// FIN MÉTODO AgentI :: notify

// MÉTODO AgentI :: _cpp_register
void
AgentI::
_cpp_register(int& explanation, int &state)
{

  string newName;

  try
    {
      ams->_cpp_register(AgentIdentifier, explanation, newName, state);
      // Se comprueba el valor de explanation.
      switch (explanation) {
	
	// Ya existe un agente en la plataforma con ese nombre.
      case Duplicate:
	// El AMS se encarga de asignar un nombre, previa solicitación del agente.
	this->setName("unknown");
	ams->_cpp_register(AgentIdentifier, explanation, newName, state);
	this->setName(newName);
	this->setNameAgentDescription(newName);
	break;

	// Registrado correctamente.
      case Success:
	break;

	// El agente no está autorizado a realizar el registro.
      case Access:
	// PENDIENTE
	break;

	// El AID no es válido.
      case Invalid:
	// El AMS se encarga de asignar un nombre, previa solicitación del agente.
	this->setName("unknown");
	ams->_cpp_register(AgentIdentifier, explanation, newName, state);
	this->setName(newName);
	this->setNameAgentDescription(newName);
	break;

      }// Fin switch

    }// Fin try
  catch (const Ice::Exception& ex)
    {
      cerr << ex << "in AgentI::_cpp_register." << endl;
    }// Fin catch

}
// FIN MÉTODO AgentI :: _cpp_register

// MÉTODO AgentI :: deregister
void
AgentI::
deregister(int& explanation)
{

  try
    {
      ams->deregister(AgentIdentifier, explanation);
      // Se comprueba el valor de explanation.
      switch (explanation) {
	
	// No existe el agente en la plataforma con ese nombre.
      case NotFound:
	// PENDIENTE
	break;

	// El agente no está autorizado a eliminar el registro.
      case Access:
	// PENDIENTE
	break;

	// Eliminado del registro correctamente.
      case Success:
	break;

	// El AID no es válido.
      case Invalid:
	// PENDIENTE
	break;

      }// Fin switch

    }// Fin try

  catch (const Ice::Exception& ex)
    {
      cerr << ex << "in AgentI::deregister." << endl;
    }// Fin catch

}
// FIN MÉTODO AgentI :: deregister

// MÉTODO AgentI :: modify
void
AgentI::
modify(TAID aid, int& explanation)
{

  try
    {
      ams->modify(aid, explanation);
      // Se comprueba el valor de explanation.
      switch (explanation) {
	
	// No existe el agente en la plataforma con ese nombre.
      case NotFound:
	// PENDIENTE
	break;

	// El agente no está autorizado a eliminar el registro.
      case Access:
	// PENDIENTE
	break;

	// Eliminado del registro correctamente.
      case Success:
	break;

	// El AID no es válido.
      case Invalid:
	// PENDIENTE
	break;

      }// Fin switch

    }// Fin try

  catch (const Ice::Exception& ex)
    {
      cerr << ex << endl;
    }// Fin catch

}
// FIN MÉTODO AgentI :: modify

// MÉTODO AgentI :: modifyDF
void
AgentI::
modifyDF(TDFAgentDescription ad, int& explanation)
{

  try
    {
      df->modify(ad, explanation);
      // Se comprueba el valor de explanation.
      switch (explanation) {
	
	// No existe el agente en la plataforma con ese nombre.
      case NotFound:
	// PENDIENTE
	break;

	// El agente no está autorizado a eliminar el registro.
      case Access:
	// PENDIENTE
	break;

	// Eliminado del registro correctamente.
      case Success:
	break;

	// El AID no es válido.
      case Invalid:
	// PENDIENTE
	break;

      }// Fin switch

    }// Fin try

  catch (const Ice::Exception& ex)
    {
      cerr << ex << endl;
    }// Fin catch

}
// FIN MÉTODO AgentI :: modifyDF

// MÉTODO AgentI :: setName
void
AgentI::
setName(string name)
{

  this->AgentIdentifier.Name = name;

}
// FIN MÉTODO AgentI :: setName

// MÉTODO AgentI :: getName
string
AgentI::
getName()
{

  return this->AgentIdentifier.Name;

}
// FIN MÉTODO AgentI :: getName

// MÉTODO AgentI :: setState
void
AgentI::
setState(int state)
{

  this->State = state;

}
// FIN MÉTODO AgentI :: setState

// MÉTODO AgentI :: getState
int
AgentI::
getState()
{

  return this->State;

}
// MÉTODO AgentI :: getState

// MÉTODO AgentI :: getAgentIdentifier
TAID
AgentI::
getAgentIdentifier()
{

  return this->AgentIdentifier;

}
// FIN MÉTODO AgentI :: getAgentIdentifier

// MÉTODO AgentI :: setNameAgentDescription
void
AgentI::
setNameAgentDescription(string name)
{

  this->AgentDescription.Name.Name = name;

}
// FIN MÉTODO AgentI :: setNameAgentDescription

// MÉTODO AgentI :: obtainServiceRoot
void
AgentI::
obtainServiceRoot()
{

  // Se obtiene un proxy del tipo StartService.
  try
    {
      startService = StartServicePrx::checkedCast(communicator()->stringToProxy("startService"));
    }// Fin try
  catch (const Ice::NotRegisteredException&)
    {
      string proxy = communicator()->getProperties()->getProperty("IceGrid.InstanceName") + "/Query";
      IceGrid::QueryPrx query = IceGrid::QueryPrx::checkedCast(communicator()->stringToProxy(proxy));
      startService = StartServicePrx::checkedCast(query->findObjectByType("::FIPA::StartService"));
    }// Fin catch
  
  if (!startService) {
    cerr << this->getName() << " --> No se pudo encontrar un objeto ::FIPA::StartService." << endl;
    return;
  }// Fin if
  
  // Se obtiene los servicios básicos.
  ServiceRoot = this->getServiceRoot();

}
// FIN MÉTODO AgentI :: obtainServiceRoot

// MÉTODO AgentI :: setContactAddress
void
AgentI::
setContactAddress(Ice::ObjectAdapterPtr& adapter)
{

  adapter = communicator()->createObjectAdapterWithEndpoints(this->getName()+"Adapter", "tcp");
  Ice::Identity ident = communicator()->stringToIdentity(this->getName());
  Ice::ObjectPrx obj = adapter->add(this, ident);
  this->addAddress(communicator()->proxyToString(obj));
  adapter->activate();

}
// FIN MÉTODO AgentI :: setContactAddress

// MÉTODO AgentI :: addAddress
void
AgentI::
addAddress(string address)
{

  AgentIdentifier.Addresses.push_back(address);

}
// FIN MÉTODO AgentI :: addAddress

// MÉTODO AgentI :: removeAddress
void
AgentI::
removeAddress(string address)
{

  int i;
  vector<string>::iterator it;

  for (i = 0; i < AgentIdentifier.Addresses.size(); i++)
    if (AgentIdentifier.Addresses[i] == address) {
      it = AgentIdentifier.Addresses.begin() + i;
      AgentIdentifier.Addresses.erase(it);
      return;
    }// Fin if

}
// FIN MÉTODO AgentI :: removeAddress

// MÉTODO AgentI :: getAgentDescription
TDFAgentDescription
AgentI::
getAgentDescription()
{

  return AgentDescription;

}
// FIN MÉTODO AgentI :: getAgentDescription

// MÉTODO AgentI :: getServices
TDFServiceDescriptions
AgentI::
getServices()
{

  return this->getAgentDescription().Services;

}
// FIN MÉTODO AgentI :: getServices

// MÉTODO AgentI :: addService
void
AgentI::
addService(string name, string type)
{

  TDFServiceDescription dFServiceDescription;
  dFServiceDescription.Name = name;
  dFServiceDescription.Type = type;
  AgentDescription.Services.push_back(dFServiceDescription);

}
// FIN MÉTODO AgentI :: addService

// MÉTODO AgentI :: getProtocols
std::vector<string>
AgentI::
getProtocols()
{

  return this->getAgentDescription().Protocols;

}
// FIN MÉTODO AgentI :: getProtocols

// MÉTODO AgentI :: addProtocol
void
AgentI::
addProtocol(string protocol)
{

  AgentDescription.Protocols.push_back(protocol);

}
// FIN MÉTODO AgentI :: addProtocol

// MÉTODO AgentI :: removeProtocol
void
AgentI::
removeProtocol(string protocol)
{

  int i;
  vector<string>::iterator it;
  
  for (i = 0; i < AgentDescription.Protocols.size(); i++)
    if (AgentDescription.Protocols[i] == protocol) {
      it = AgentDescription.Protocols.begin() + i;
      AgentDescription.Protocols.erase(it);
      return;
    }// Fin if

}
// MÉTODO AgentI :: removeProtocol

// MÉTODO AgentI :: getBasicServiceAMS
void
AgentI::
getBasicServiceAMS(int i)
{

  int explanation;

  // Se obtiene una referencia al AMS.
  ams = AMSPrx::checkedCast(communicator()->stringToProxy(ServiceRoot[i].ServiceLocator[0].ServiceAddress));
  cout << this->getName() << " --> He obtenido una referencia al AMS." << endl;
      
  // El agente se registra en la plataforma de agentes a través del AMS.
  this->_cpp_register(explanation, State);

  // Se comprueba si ha habido éxito en el registro.
  if (explanation == Success)
    cout << this->getName() << " --> Registrado en la plataforma." << endl;
  else
    cout << this->getName() << " --> Fue incapaz de registrarse en la plataforma." << endl;

  cout << this->getName() << " --> Mi estado es " << State << endl;

}
// FIN MÉTODO AgentI :: getBasicServiceAMS

// MÉTODO AgentI :: getBasicServiceDF
void
AgentI::
getBasicServiceDF(IceStorm::TopicPrx& topic, Ice::ObjectPrx& proxy, Ice::ObjectAdapterPtr& adapter, int i)
{

  // Se obtiene una referencia al DirectoryFacilitator.
  df = DirectoryFacilitatorPrx::checkedCast(communicator()->stringToProxy(ServiceRoot[i].ServiceLocator[0].ServiceAddress));
  cout << this->getName() << " --> He obtenido una referencia al DirectoryFacilitator." << endl;
  // Subscripción al DirectoryFacilitator.
  this->subscribeDF(topic, proxy, adapter);

}
// FIN MÉTODO AgentI :: getBasicServiceDF

// MÉTODO AgentI :: getBasicServiceACC
void
AgentI::
getBasicServiceACC(Ice::ObjectAdapterPtr& adapter, int i)
{

  // Se obtiene una referencia al ACC.
  acc = ACCPrx::checkedCast(communicator()->stringToProxy(ServiceRoot[i].ServiceLocator[0].ServiceAddress));
  cout << this->getName() << " --> He obtenido una referencia al ACC." << endl;

}
// FIN MÉTODO AgentI :: getBasicServiceACC

// MÉTODO AgentI :: subscribeDF
void
AgentI::
subscribeDF(IceStorm::TopicPrx& topic, Ice::ObjectPrx& proxy, Ice::ObjectAdapterPtr& adapter)
{

  int explanation = Success;

  // Mecanismo de subscripción con IceStorm.
  Ice::ObjectPrx obj = communicator()->stringToProxy("DirectoryFacilitator/TopicManager:tcp -p 9999");
  IceStorm::TopicManagerPrx topicManager = IceStorm::TopicManagerPrx::checkedCast(obj);
  proxy = adapter->addWithUUID(this);
    
  try
    {
      topic = topicManager->retrieve("Agent");
      IceStorm::QoS qos;
      cout << "Agente " << this->getName() << " subscribiéndose al DirectoryFacilitator." << endl;
      topic->subscribe(qos, proxy);
    }// Fin try
  catch(const IceStorm::NoSuchTopic&)
    {
      topic = topicManager->create("Agent");
    }// Fin catch
  
  adapter->activate();
  
  // El agente se subscribe al servicio DirectoryFacilitator.
  df->_cpp_register(AgentDescription, explanation);
  
  // Se comprueba si ha habido éxito en el registro con el DirectoryFacilitator.
  if (explanation == Success)
    cout << this->getName() << " --> Registrado en el DirectoryFacilitator." << endl;
  else
    cout << this->getName() << " --> No se pudo registrar en el DirectoryFacilitator." << endl;

}
// FIN MÉTODO AgentI :: subscribeDF

// MÉTODO AgentI :: unsubscribeDF
void
AgentI::
unsubscribeDF(IceStorm::TopicPrx& topic, Ice::ObjectPrx& proxy)
{

  int explanation = Success;

  try
    {
      topic->unsubscribe(proxy);
    }// Fin try
  catch(const IceStorm::NoSuchTopic&)
    {
      cout << this->getName() << " --> No se pudo dar de baja del DirectoryFacilitator" << endl;
    }// Fin catch

  // El agente elimina su registro del servicio DirectoryFacilitator.
  df->deregister(AgentDescription, explanation);
  
  // Se comprueba si ha habido éxito en la eliminación del registro con el DirectoryFacilitator.
  if (explanation == Success)
    cout << this->getName() << " --> Dado de baja en el DirectoryFacilitator." << endl;
  else
    cout << this->getName() << " --> No se pudo dar de baja en el DirectoryFacilitator." << endl;

}
// FIN MÉTODO AgentI :: unsubscribeDF

// MÉTODO AgentI :: getBasicServices
void
AgentI::
getBasicServices(IceStorm::TopicPrx& topic, Ice::ObjectPrx& proxy, Ice::ObjectAdapterPtr& adapter)
{

  int i;

  // Se recorren los servicios básicos para obtener referencias a ellos.
  for (i = 0; i < ServiceRoot.size(); i++) {
    
    // Se obtiene un proxy AMS
    if (ServiceRoot[i].ServiceType == "::FIPA::AMS" && !ams)
      this->getBasicServiceAMS(i);

    // Se obtiene un proxy DirectoryFacilitator
    if (ServiceRoot[i].ServiceType == "::FIPA::DirectoryFacilitator" && !df)
      this->getBasicServiceDF(topic, proxy, adapter, i);

    // Se obtiene un proxy ACC
    if (ServiceRoot[i].ServiceType == "::FIPA::ACC" && !acc)
      this->getBasicServiceACC(adapter, i);

  }// Fin for

}
// FIN MÉTODO AgentI :: getBasicServices

// MÉTODO AgentI:: send
void
AgentI::
send(string performative, TAIDs to, int ACLRepresentation, string payload, string language, string protocol, string idConv)
{

  TMessage message;
  TEnvelope envelope;
  TDate date;
  ACLMessage *aclMessage;
  string out;

  // PENDIENTE
  date.hour = 0;
  date.minutes = 0;
  date.seconds = 0;
  envelope.To = to;
  envelope.From = this->getAgentIdentifier();
  envelope.Date = date;
  envelope.ACLRepresentation = ACLRepresentation;
  message.Envelope = envelope;

  // Creación del mensaje ACL según la representación aclRepresentation.
  aclMessage = new ACLMessage(performative, to, this->getAgentIdentifier(), ACLRepresentation, language, payload, protocol, idConv);
  if (!aclMessage->createFIPAACLMessage(out)) {
    message.Payload = out;
    this->send(message);
  }// Fin if

}
// FIN MÉTODO AgentI:: send
 
// MÉTODO AgentI:: send
void
AgentI::
send(TMessage message)
{

  try
    {
      acc->receive(message);
    }// Fin try
  catch (const Ice::Exception& ex)
    {
      cout << "Falla aquí..." << endl;
      cerr << ex << endl;
    }// Fin catch

}
// FIN MÉTODO AgentI:: send

// MÉTODO AgentI :: receiveACLMessage
void
AgentI::
receiveACLMessage(const ::std::string& message, const ::Ice::Current&)
{

  bool errorsOccured;

  try
    {
      // Inicialización del sistema
      XMLPlatformUtils::Initialize();
    }
  
  catch(const XMLException& toCatch)
    {
      char *pMsg = XMLString::transcode(toCatch.getMessage());
      XERCES_STD_QUALIFIER cerr << "Error al inicializar xerces-c.\n"
				<< "  Mensaje de excepción:"
				<< pMsg;
      XMLString::release(&pMsg);
      return ;
    }// Fin catch
  
  try
    {
      
      cout << message << endl;

      // Se almacena el contenido del mensaje en un archivo para realizar el parser.
      // PENDIENTE --> Pasar directamente de string a DOMDocument
      ofstream fout(this->getName().c_str());
      fout << message;
      fout.close();

      // Objetos necesarios para el parser.
      DOMImplementation* impl =  DOMImplementationRegistry::getDOMImplementation(X("Core"));
      DOMBuilder *parser = impl->createDOMBuilder(DOMImplementation::MODE_SYNCHRONOUS, 0);
            
      // Parseado.
      DOMDocument *doc = parser->parseURI(this->getName().c_str());
      DOMElement *raiz = doc->getDocumentElement();

      // PENDIENTE

      const XMLCh *buf = raiz->getAttribute(X("act"));
      char *salida = XMLString::transcode(buf);
      string s1(salida);
      cout << s1 << endl;
      
    }// Fin try
  
  catch (const OutOfMemoryException&)
    {
      XERCES_STD_QUALIFIER cerr << "Error debido a falta de memoria." << XERCES_STD_QUALIFIER endl;
      errorsOccured = true;
    }// Fin catch
  catch (const XMLException& e)
    {
      XERCES_STD_QUALIFIER cerr << "Error en el parser\n   Mensaje: "
				<< e.getMessage() << XERCES_STD_QUALIFIER endl;
      errorsOccured = true;
    }// Fin catch
  
  catch (const DOMException& e)
    {
      const unsigned int maxChars = 2047;
      XMLCh errText[maxChars + 1];
      
      XERCES_STD_QUALIFIER cerr << "\nError en el parser: '" << this->getName() << "'\n"
				<< "DOMException code is:  " << e.code << XERCES_STD_QUALIFIER endl;
      
      if (DOMImplementation::loadDOMExceptionMsg(e.code, errText, maxChars))
	XERCES_STD_QUALIFIER cerr << "Mensaje: " << errText << XERCES_STD_QUALIFIER endl;
      
      errorsOccured = true;
    }// Fin catch
  
  catch (...)
    {
      XERCES_STD_QUALIFIER cerr << "Error en el parser\n " << XERCES_STD_QUALIFIER endl;
      errorsOccured = true;
    }// Fin catch

  XMLPlatformUtils::Terminate();
  
}
// FIN MÉTODO AgentI :: receiveACLMessage

// METODO AgentI :: run
int
AgentI::
run(int argc, char *argv[])
{

  int i, j;
  int explanation = Invalid;
  Ice::ObjectAdapterPtr adapter;
  IceStorm::TopicPrx topic;
  Ice::ObjectPrx proxy;

  this->obtainServiceRoot();
  this->setContactAddress(adapter);

  this->getBasicServices(topic, proxy, adapter);

  //sleep(5);
  //AgentDescription.LeaseTime = 36000;
  //this->modifyDF(AgentDescription, explanation);

  string performative("request");
  int aclRep = xmlRep;
  string content("Contenido");
  string language("PorDefinir");
  string protocol("Uknown");
  string idConv("742");
  TAIDs to;
  to.push_back(this->getAgentIdentifier());

  //ACLMessage *message = new ACLMessage(performative, to, this->getAgentIdentifier(), aclRep, language, content, protocol, idConv);
  //string m;
  //message->createFIPAACLMessage(m);
  //cout << m << endl;

  //string act("investigate");
  //vector<string> arguments;
  //arguments.push_back("X-Files");
  //ContentRDF::createAction(act, this->getName(), arguments, m);
  //cout << "\n" << m << endl;
  this->send(performative, to, aclRep, content, language, protocol, idConv);

  sleep(15);

  this->deregister(explanation);
  this->unsubscribeDF(topic, proxy);
  communicator()->waitForShutdown();
  
  return EXIT_SUCCESS;
  
}
// FIN METODO AgentI :: run

// METODO main
int
main(int argc, char *argv[])
{

  // Se comprueba que el agente tiene nombre.
  if (argc < 2)
    cout << "Necesito un nombre para ser un agente." << endl;
  else {
    AgentI *agent = new AgentI(argv[1]);
    return agent->main(argc, argv, "config/agent.cfg");
  }// Fin else

}
// FIN METODO main
