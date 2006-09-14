/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fern�ndez *************************/
/************************************************************/

#include <iostream>
#include <FIPA.h>
#include <Util.h>
#include <InputService.hpp>
#include <Ice/Ice.h>
#include <Ice/IdentityUtil.h>

using namespace std;
using namespace FIPA;

class Service
{
  
public:
  
  Service();
  ~Service();
  
  void init(string inputFileXML);
  string getServiceType();
  string getServiceId();
  TServiceLocator getServiceLocator();
  string getDescription();

protected:
  
  // ServiceDirectoryEntry es la descripci�n del servicio StartService.
  TServiceDirectoryEntry ServiceDirectoryEntry;
  // Description representa la descripci�n textual del servicio StartService.
  string Description;

};
