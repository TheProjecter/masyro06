/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <ContentRDF.h>

// MÉTODO ContentRDF :: createAction
int
ContentRDF::
createAction(string act, string actor, vector<string> arguments, string &content)
{

  vector<string>::iterator it;
  int errorCode = 0;

  try
    {
      // Inicialización del sistema.
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

	// *** rdf:RDF es la raíz del mensaje.
	DOMDocument *action = impl->createDocument(0, X("RDF"), 0);
	action->setEncoding(X("UTF-8"));

	// *** Comentario inicial.
	//action->createComment(X("<?xml version=\"1.0\" standalone=\"no\">"));
	//action->createComment(X("<!DOCTYPE fipa-message SYSTEM \"aclRep.dtd\">"));
	
	// *** Atributos de rdf:RDF.
	DOMElement* rootElem = action->getDocumentElement();
	rootElem->setAttribute(X("xmlnsrdf"), X("http://www.w3.org/1999/02/22-rdf-syntax.ns#"));
	rootElem->setAttribute(X("xmlnsfipa"), X("http://www.fipa.org/schemas/fipa-rdf0#"));
	
	DOMElement* actionElem = action->createElement(X("Action"));
	rootElem->appendChild(actionElem);
	actionElem->setAttribute(X("ID"), X((actor + "Action").c_str()));
	
	// *** Actor.
	DOMElement* actorElem = action->createElement(X("Actor"));
	actionElem->appendChild(actorElem);
	DOMText* actorText = action->createTextNode(X(actor.c_str()));
	actorElem->appendChild(actorText);

	// *** Act.
	DOMElement* actElem = action->createElement(X("Act"));
	actionElem->appendChild(actElem);
	DOMText* actText = action->createTextNode(X(act.c_str()));
	actElem->appendChild(actText);

	// *** Arguments.
	DOMElement* argumentsElem = action->createElement(X("Argument"));
	actionElem->appendChild(argumentsElem);
	DOMElement* bagElem = action->createElement(X("Bag"));
	argumentsElem->appendChild(bagElem);

	// Lista de argumentos.
	DOMElement* argumentElem;
	DOMText* argumentText;

	for (it = arguments.begin(); it != arguments.end(); it++) {
	  argumentElem = action->createElement(X("Li"));
	  bagElem->appendChild(argumentElem);
	  argumentText = action->createTextNode(X((*it).c_str()));
	  argumentElem->appendChild(argumentText);
	}// Fin for

	// Serialización a través de DOMWriter
	XMLCh tempStr[100];
	XMLString::transcode("LS", tempStr, 99);
	DOMImplementation *impl = DOMImplementationRegistry::getDOMImplementation(tempStr);
	DOMWriter *theSerializer = ((DOMImplementationLS*)impl)->createDOMWriter();

	// Conversión a string
	XMLCh *buf = theSerializer->writeToString(*action);
	char *salida = XMLString::transcode(buf);
	string s1(salida);
	content = s1;
	
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
// FIN MÉTODO ContentRDF :: createAction

// MÉTODO ContentRDF :: createProposition
int
ContentRDF::
createProposition(string subject, string predicate, string object, string &content)
{

  int errorCode = 0;

  try
    {
      // Inicialización del sistema.
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

	// *** rdf:RDF es la raíz del mensaje.
	DOMDocument *action = impl->createDocument(0, X("RDF"), 0);
	action->setEncoding(X("UTF-8"));

	// *** Comentario inicial.
	//action->createComment(X("<?xml version=\"1.0\" standalone=\"no\">"));
	//action->createComment(X("<!DOCTYPE fipa-message SYSTEM \"aclRep.dtd\">"));
	
	// *** Atributos de rdf:RDF.
	DOMElement* rootElem = action->getDocumentElement();
	rootElem->setAttribute(X("xmlnsrdf"), X("http://www.w3.org/1999/02/22-rdf-syntax.ns#"));
	rootElem->setAttribute(X("xmlnsfipa"), X("http://www.fipa.org/schemas/fipa-rdf0#"));
	
	DOMElement* descElem = action->createElement(X("rdfDescription"));
	rootElem->appendChild(descElem);
	descElem->setAttribute(X("ID"), X((subject).c_str()));
	
	// *** Predicate.
	DOMElement* predicateElem = action->createElement(X(predicate.c_str()));
	descElem->appendChild(predicateElem);
	DOMText* predicateText = action->createTextNode(X(object.c_str()));
	predicateElem->appendChild(predicateText);

	// Serialización a través de DOMWriter
	XMLCh tempStr[100];
	XMLString::transcode("LS", tempStr, 99);
	DOMImplementation *impl = DOMImplementationRegistry::getDOMImplementation(tempStr);
	DOMWriter *theSerializer = ((DOMImplementationLS*)impl)->createDOMWriter();

	// Conversión a string
	XMLCh *buf = theSerializer->writeToString(*action);
	char *salida = XMLString::transcode(buf);
	string s1(salida);
	content = s1;
	
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
// FIN MÉTODO ContentRDF :: createProposition
