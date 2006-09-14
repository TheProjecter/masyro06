/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <ACLMessage.h>

// MÉTODO ACLMessage :: ACLMessage
ACLMessage::
ACLMessage(string performative, TAIDs to, TAID from, int aclRepresentation, string language, string content, string protocol, string idConv)
{

  Performative = performative;
  To = to;
  From = from;
  ACLRepresentation = aclRepresentation;
  Language = language;
  Content = content;
  Protocol = protocol;
  IDConv = idConv;

}
// FIN MÉTODO ACLMessage :: ACLMessage

// MÉTODO ACLMessage :: ~ACLMessage
ACLMessage::
~ACLMessage()
{
}
// FIN MÉTODO ACLMessage :: ~ACLMessage

// MÉTODO ACLMessage :: createFIPAACLMessage
int
ACLMessage::
createFIPAACLMessage(string &mensaje)
{

  switch (this->getACLRepresentation()) {
    
  case bitefficientRep:
    return this->createFIPAACLMessageBitEfficient(mensaje);
    break;
  case stringRep:
    return this->createFIPAACLMessageString(mensaje);
    break;
  case xmlRep:
    return this->createFIPAACLMessageXML(mensaje);
    break;
    
  }// Fin switch

}
// FIN MÉTODO ACLMessage :: createFIPAACLMessage

// MÉTODO ACLMessage :: createFIPAACLMessageBitEfficient
int
ACLMessage::
createFIPAACLMessageBitEfficient(string &mensaje)
{
  // PENDIENTE
}
// FIN MÉTODO ACLMessage :: createFIPAACLMessageBitEfficient

// MÉTODO ACLMessage :: createFIPAACLMessageString
int
ACLMessage::
createFIPAACLMessageString(string &mensaje)
{
  // PENDIENTE
}
// FIN MÉTODO ACLMessage :: createFIPAACLMessageString

// MÉTODO ACLMessage :: createFIPAACLMessageXLM
int
ACLMessage::
createFIPAACLMessageXML(string &mensaje)
{
  
  int i, j, errorCode = 0;

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
      return 1;
    }// Fin catch
  
  DOMImplementation* impl =  DOMImplementationRegistry::getDOMImplementation(X("Core"));
  
  if (impl != NULL) {
    
    try
      {

	// *** fipa-message es la raíz del mensaje.
	DOMDocument *aclMessage = impl->createDocument(0, X("fipa-message"), 0);
	aclMessage->setEncoding(X("UTF-8"));

	// *** Comentario inicial
	//aclMessage->createComment(X("<?xml version=\"1.0\" standalone=\"no\">"));
	//aclMessage->createComment(X("<!DOCTYPE fipa-message SYSTEM \"aclRep.dtd\">"));
	
	// *** Tipo de mensaje.
	DOMElement* rootElem = aclMessage->getDocumentElement();
	rootElem->setAttribute(X("act"), X(this->getPerformative().c_str()));
	
	// *** Emisor del mensaje.
	DOMElement*  senderElem = aclMessage->createElement(X("sender"));
	rootElem->appendChild(senderElem);
	
	DOMElement*  agentIdentifierElem = aclMessage->createElement(X("agent-identifier"));
	senderElem->appendChild(agentIdentifierElem);
	
	// Nombre del agente emisor del mensaje.
	DOMElement*  nameElem = aclMessage->createElement(X("name"));
	agentIdentifierElem->appendChild(nameElem);
	nameElem->setAttribute(X("id"), X(this->getFrom().Name.c_str()));
	
	// Dirección/es del agente emisor del mensaje.
	DOMElement*  addressesElem = aclMessage->createElement(X("addresses"));
	DOMElement*  urlElem;
	agentIdentifierElem->appendChild(addressesElem);
	
	for (i = 0; i < this->getFrom().Addresses.size(); i++) {
	  urlElem = aclMessage->createElement(X("url"));
	  addressesElem->appendChild(urlElem);
	  urlElem->setAttribute(X("href"), X(this->getFrom().Addresses[i].c_str()));
	}// Fin for

	// *** Receptor/es del mensaje.
	DOMElement* receiverElem = aclMessage->createElement(X("receiver"));
	rootElem->appendChild(receiverElem);
	
	// Nombre/s y dirección/es del agente o agentes receptor/es.
	for (i = 0; i < this->getTo().size(); i++) {
	  agentIdentifierElem = aclMessage->createElement(X("agent-identifier"));
	  receiverElem->appendChild(agentIdentifierElem);
	  // Nombre.
	  nameElem = aclMessage->createElement(X("name"));
	  agentIdentifierElem->appendChild(nameElem);
	  nameElem->setAttribute(X("id"), X(this->getTo()[i].Name.c_str()));
	  addressesElem = aclMessage->createElement(X("addresses"));
	  agentIdentifierElem->appendChild(addressesElem);
	  // Direcciones de contacto.
	  for (j = 0; j < this->getTo()[i].Addresses.size(); j++) {
	    urlElem = aclMessage->createElement(X("url"));
	    addressesElem->appendChild(urlElem);
	    urlElem->setAttribute(X("href"), X(this->getTo()[i].Addresses[j].c_str()));
	  }// Fin for
	}// Fin for

	// *** Contenido del mensaje.
	DOMElement* contentElem = aclMessage->createElement(X("content"));
	rootElem->appendChild(contentElem);
	DOMText* contentText = aclMessage->createTextNode(X(this->getContent().c_str()));
	contentElem->appendChild(contentText);

	// *** Lenguaje del mensaje.
	DOMElement* languageElem = aclMessage->createElement(X("language"));
	rootElem->appendChild(languageElem);
	DOMText* languageText = aclMessage->createTextNode(X(this->getLanguage().c_str()));
	languageElem->appendChild(languageText);

	// *** Procotolo de comunicación del mensaje.
	DOMElement* protocolElem = aclMessage->createElement(X("protocol"));
	rootElem->appendChild(protocolElem);
	DOMText* protocolText = aclMessage->createTextNode(X(this->getProtocol().c_str()));
	protocolElem->appendChild(protocolText);

	// *** Identificador de la conversación asociada al mensaje.
	DOMElement* idConvElem = aclMessage->createElement(X("conversation-id"));
	rootElem->appendChild(idConvElem);
	DOMText* idConvText = aclMessage->createTextNode(X(this->getIDConv().c_str()));
	idConvElem->appendChild(idConvText);

	// Serialización a través de DOMWriter
	XMLCh tempStr[100];
	XMLString::transcode("LS", tempStr, 99);
	DOMImplementation *impl = DOMImplementationRegistry::getDOMImplementation(tempStr);
	DOMWriter *theSerializer = ((DOMImplementationLS*)impl)->createDOMWriter();

	// Conversión a string
	XMLCh *buf = theSerializer->writeToString(*aclMessage);
	char *salida = XMLString::transcode(buf);
	string s1(salida);
	mensaje = s1;
	
	XMLString::release(&buf);
	XMLString::release(&salida);

	delete theSerializer;

	XMLPlatformUtils::Terminate();

      }// Fin try
    
    catch (const OutOfMemoryException&)
      {
	XERCES_STD_QUALIFIER cerr << "Error debido a falta de memoria." << XERCES_STD_QUALIFIER endl;
	errorCode = 5;
      }// Fin catch
    catch (const DOMException& e)
      {
	XERCES_STD_QUALIFIER cerr << "DOMException en:  " << e.code << XERCES_STD_QUALIFIER endl;
	errorCode = 2;
      }// Fin catch
    catch (...)
      {
	XERCES_STD_QUALIFIER cerr << "Se produjo un error al crear el mensaje ACL." << XERCES_STD_QUALIFIER endl;
	errorCode = 3;
      }// Fin catch

  }// Fin if

  else {
    XERCES_STD_QUALIFIER cerr << "La implementación requerida no está disponible." << XERCES_STD_QUALIFIER endl;
    errorCode = 4;
  }// Fin else
    
  XMLPlatformUtils::Terminate();
  return errorCode;

}
// FIN MÉTODO ACLMessage :: createFIPAACLMessageXML

// MÉTODO ACLMessage :: getPerformative
string
ACLMessage::
getPerformative()
{

  return Performative;

}
// FIN MÉTODO ACLMessage :: getPerformative

// MÉTODO ACLMessage :: getTo
TAIDs
ACLMessage::
getTo()
{

  return To;

}
// FIN MÉTODO ACLMessage :: getTo

// MÉTODO ACLMessage :: getFrom
TAID
ACLMessage::
getFrom()
{

  return From;

}
// FIN MÉTODO ACLMessage :: getFrom

// MÉTODO ACLMessage :: getACLRepresentation
int
ACLMessage::
getACLRepresentation()
{

  return ACLRepresentation;

}
// FIN MÉTODO ACLMessage :: getACLRepresentation

// MÉTODO ACLMessage :: getLanguage
string
ACLMessage::
getLanguage()
{

  return Language;

}
// FIN MÉTODO ACLMessage :: getLanguage

// MÉTODO ACLMessage :: getContent
string
ACLMessage::
getContent()
{

  return Content;

}
// FIN MÉTODO ACLMessage :: getContent

// MÉTODO ACLMessage :: getProtocol
string
ACLMessage::
getProtocol()
{

  return Protocol;

}
// FIN MÉTODO ACLMessage :: getProtocol

// MÉTODO ACLMessage :: getIDConv
string
ACLMessage::
getIDConv()
{

  return IDConv;

}
// FIN MÉTODO ACLMessage :: getIDConv
