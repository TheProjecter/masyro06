/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <InputService.hpp>

// MÉTODO InputService :: InputService
InputService::
InputService(string file)
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

      int i, j;
      DOMElement *el;
      DOMNode *node, *locator, *att;
      DOMNamedNodeMap *attributes;
      DOMNodeList *locators;
      XMLCh tempStr[100];
      TServiceLocationDescription sld;
      char *ch;
      string str, grammar = "service.dtd";

      // Objetos necesarios para el parser.
      DOMImplementation* impl =  DOMImplementationRegistry::getDOMImplementation(X("Core"));
      DOMBuilder *parser = impl->createDOMBuilder(DOMImplementation::MODE_SYNCHRONOUS, 0);

      parser->loadGrammar(grammar.c_str(), 1, true);

      // Se parsea el fichero.
      Doc = parser->parseURI(file.c_str());

      // Se obtiene el elemento raíz.
      DOMElement *root = Doc->getDocumentElement();
      XMLString::transcode("name", tempStr, 99);
      // Se obtiene el nombre del servicio.
      ch = XMLString::transcode(root->getAttribute(tempStr));
      ServiceName = ch;

      // Se obtienen los hijos del nodo raíz --> serviceDirectoryEntry, description
      DOMNodeList *childs = root->getChildNodes();

      for (i = 0; i < childs->getLength(); i++) {
	node = childs->item(i);
	ch = XMLString::transcode(node->getNodeName());
	str = ch;

	if (str == "serviceDirectoryEntry") {

	  // Se obtienen las direcciones de los servicios.
	  locators = node->getChildNodes();
	  for (j = 0; j < locators->getLength(); j++) {

	    locator = locators->item(j);
	    ch = XMLString::transcode(locator->getNodeName());
	    str = ch;

	    if (str == "serviceLocator") {
	      attributes = locator->getAttributes();
	      XMLString::transcode("serviceSignature", tempStr, 99);
	      att = attributes->getNamedItem(tempStr);
	      // Se obtiene la signatura.
	      ch = XMLString::transcode(att->getNodeValue());
	      sld.ServiceSignature = ch;
	      XMLString::transcode("serviceAddress", tempStr, 99);
	      att = attributes->getNamedItem(tempStr);
	      // Se obtiene la dirección.
	      ch = XMLString::transcode(att->getNodeValue());
	      sld.ServiceAddress = ch;
	      ServiceLocator.push_back(sld);
	    }// Fin if

	  }// Fin for

	  attributes = node->getAttributes();
	  XMLString::transcode("serviceType", tempStr, 99);
	  att = attributes->getNamedItem(tempStr);
	  // Se obtiene el tipo del servicio.
	  ch = XMLString::transcode(att->getNodeValue());
	  ServiceType = ch;
	  XMLString::transcode("serviceId", tempStr, 99);
	  att = attributes->getNamedItem(tempStr);
	  // Se obtiene el id del servicio.
	  ch = XMLString::transcode(att->getNodeValue());
	  ServiceId = ch;

	}// Fin if serviceDirectoryEntry

	if (str == "description") {
	  att = node->getFirstChild();
	  ch = XMLString::transcode(att->getNodeValue());
	  Description = ch;
	}// Fin if

      }// Fin for

      delete parser;

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
      
      XERCES_STD_QUALIFIER cerr << "\nError en el parser: '" << this->getServiceId() << "'\n"
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
// FIN MÉTODO InputService :: InputService

// MÉTODO InputService :: ~InputService
InputService::
~InputService()
{
}
// FIN MÉTODO InputService :: ~InputService

// MÉTODO InputService :: getServiceName
string
InputService::
getServiceName()
{

  return ServiceName;

}
// FIN MÉTODO InputService :: getServiceName

// MÉTODO InputService :: getServiceType
string
InputService::
getServiceType()
{

  return ServiceType;

}
// FIN MÉTODO InputService :: getServiceType

// MÉTODO InputService :: getServiceId
string
InputService::
getServiceId()
{

  return ServiceId;

}
// FIN MÉTODO InputService :: getServiceId

// MÉTODO InputService :: getServiceLocator
TServiceLocator
InputService::
getServiceLocator()
{

  return ServiceLocator;

}
// FIN MÉTODO InputService :: getServiceLocator

// MÉTODO InputService :: getDescription
string
InputService::
getDescription()
{

  return Description;

}
// FIN MÉTODO InputService :: getDescription
