/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#ifndef INPUTSERVICE
#define INPUTSERVICE

#include <FIPA.h>
#include <Util.h>
#include <cstring>
#include <fstream>
#include <DOMBuilder.hpp>
#include <AbstractDOMParser.hpp>

using namespace std;
using namespace FIPA;

// CLASE InputService
class InputService
{

 public:

  InputService(string file);
  ~InputService();

  string getServiceName();
  string getServiceType();
  string getServiceId();
  TServiceLocator getServiceLocator();
  string getDescription();
  
 private:
  
  DOMDocument *Doc;
  string ServiceName;
  string ServiceType;
  string ServiceId;
  TServiceLocator ServiceLocator;
  string Description;
  
};
// FIN CLASE InputService

#endif
