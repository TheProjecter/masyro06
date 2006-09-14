/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <Service.hpp>

Service::
Service()
{
}

Service::
~Service()
{
}

void
Service::
init(string inputFileXML)
{

  InputService is = InputService(inputFileXML);

  ServiceDirectoryEntry.ServiceType = is.getServiceType();
  ServiceDirectoryEntry.ServiceId = is.getServiceId();
  ServiceDirectoryEntry.ServiceLocator = is.getServiceLocator();
  Description = is.getDescription();

}

string
Service::
getServiceType()
{

  return ServiceDirectoryEntry.ServiceType;

}

string
Service::
getServiceId()
{

  return ServiceDirectoryEntry.ServiceId;

}

TServiceLocator
Service::
getServiceLocator()
{

  return ServiceDirectoryEntry.ServiceLocator;

}

::std::string
Service::
getDescription()
{

  return Description;

}

