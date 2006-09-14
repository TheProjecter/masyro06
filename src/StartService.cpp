/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <StartService.h>

StartServiceI::
StartServiceI()
{
}

StartServiceI::
~StartServiceI()
{
}

::FIPA::TServiceDirectoryEntries
StartServiceI::
getServiceRoot(const ::Ice::Current&) const
{
  
  return ServiceRoot;

}

void 
StartServiceI::
supplyBasicService(const ::FIPA::TServiceDirectoryEntry& sde, const ::Ice::Current&)
{

  // Se comprueba si ya existe un servicio con el mismo nombre.
  if (!Util::existService(sde, ServiceRoot)) {
    ServiceRoot.push_back(sde);
    cout << "StartService --> Registro de un nuevo servicio: " << sde.ServiceId << " del tipo: " << sde.ServiceType << endl;
  }// Fin if
  else
    cout << "StartService --> Ya existe un servicio con el nombre " << sde.ServiceId << endl;

}

void
StartServiceI::
registerAsWKO()
{

  // Registro de StartService como objeto bien conocido.
  Ice::PropertiesPtr properties = communicator()->getProperties();
  Ice::ObjectAdapterPtr adapter = communicator()->createObjectAdapter("StartServiceAdapter");
  Ice::Identity id = communicator()->stringToIdentity(properties->getProperty("IdentitySS"));

  // Se inicializan los parámetros básicos del servicio.
  this->init(properties->getProperty("InputSS"));

  adapter->add(this, id);
  adapter->activate();

}

int
StartServiceI::
run(int argc, char *argv[])
{

  try
    {

      // Desde el punto de vista de la implementación, registro de StarService como objeto bien conocido.
      this->registerAsWKO();
      // Suspensión del hilo de ejecución hasta que termina la ejecución del servidor.
      communicator()->waitForShutdown();
      
      return EXIT_SUCCESS;
      
    }// Fin try
  
  catch (const Ice::Exception& ex)
    {
      cerr << ex << " in StartServiceI::run." << endl;
      return EXIT_FAILURE;
    }// Fin catch

}

int
main(int argc, char *argv[])
{

  StartServiceI sti;
  return sti.main(argc, argv);
  
}

