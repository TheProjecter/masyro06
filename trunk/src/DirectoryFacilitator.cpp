/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <DirectoryFacilitator.h>

DirectoryFacilitatorI::
DirectoryFacilitatorI()
{
}

DirectoryFacilitatorI::
~DirectoryFacilitatorI()
{
}

void
DirectoryFacilitatorI::
_cpp_register(const ::FIPA::TDFAgentDescription& ad, ::Ice::Int& explanation, const ::Ice::Current&)
{

  int i;

  // Se comprueba que no existe un agente con el mismo nombre registrado en el DirectoryFacilitator.
  if (Util::isAgentRegisteredDF(ad.Name.Name, AgentDirectory)) {
    explanation = Duplicate;
    cout << "DirectoryFacilitator --> El agente " << ad.Name.Name << " ya existe en el DirectoryFacilitator." << endl;
  }// Fin if
  else {
    // Se registra el nuevo agente y se da de alta junto al resto de agentes.
    cout << "DirectoryFacilitator --> Registro del agente: " << ad.Name.Name << endl;
    AgentDirectory.push_back(ad);      
    explanation = Success;

  }// Fin else
  
}

void
DirectoryFacilitatorI::
deregister(const ::FIPA::TDFAgentDescription& ad, ::Ice::Int& explanation, const ::Ice::Current&)
{

  // Se comprueba si el agente estaba registrado en el DirectoryFacilitator de la plataforma MASYRO.
  if (!Util::removeRegisteredAgentDF(ad.Name.Name, AgentDirectory)) {
    explanation = NotFound;
    cout << "DirectoryFacilitator --> El agente " << ad.Name.Name << " no está registrado." << endl;
  }// Fin if
  else {
    cout << "DirectoryFacilitator --> El agente " << ad.Name.Name << " elimina su registro." << endl;
    explanation = Success;

  }// Fin else

}

void
DirectoryFacilitatorI::
modify(const ::FIPA::TDFAgentDescription& ad, ::Ice::Int& explanation, const ::Ice::Current&)
{
  
  // Se comprueba que el ad está en el registro.
  if (!Util::isAgentRegisteredDF(ad.Name.Name, AgentDirectory)) {
    cout << "DirectoryFacilitator --> El agente " << ad.Name.Name << " no está registrado." << endl;
    explanation = NotFound;
  }// Fin if
  else
    if (!Util::modifyRegisteredAgentDF(ad, AgentDirectory)) {
      cout << "DirectoryFacilitator --> No puedo modificar datos del agente " << ad.Name.Name << endl;
      explanation = Invalid;
    }// Fin if
    else {
      explanation = Success;
    }// Fin else

}

void
DirectoryFacilitatorI::
search(const ::FIPA::TDFAgentDescription& ad, ::Ice::Int match, ::Ice::Int& explanation, ::FIPA::TDFAgentDescriptions& ads, const ::Ice::Current&) const
{

  int i;

  switch (match) {
    
    // Matchin total.
  case SAME:
    // Se recorre el AgentDirectory para ver si existe un agente con el nombre proporcionado.
    for (i = 0; i < AgentDirectory.size(); i++)
      if (ad.Name.Name == AgentDirectory[i].Name.Name)
	ads.push_back(AgentDirectory[i]);
    break;

    // Matching parcial --> Búsqueda de agentes que proporcionen un determinado servicio.
  case ANY:
    for (i = 0; i < AgentDirectory.size(); i++)
      if (Util::existsAgentService(ad.Services[0].Type, AgentDirectory[i]))
	ads.push_back(AgentDirectory[i]);
    break;

  }// Fin switch
  
  if (ads.size() == 0)
    explanation = NotFound;
  else
    explanation = Success;

}

int
DirectoryFacilitatorI::
supplyBasicService()
{
  
  try
    {    
      startService->supplyBasicService(ServiceDirectoryEntry); 
    }// Fin try
 
  catch (const Ice::Exception& ex)
    {
      cerr << ex << " in DirectoryFacilitatorI::supplyBasicService." << endl;
    }// Fin catch 
 
}

void
DirectoryFacilitatorI::
registerAsBasicService()
{

  // Se obtiene un proxy del tipo StartService.
  try
    {
      startService = StartServicePrx::checkedCast(communicator()->stringToProxy("startService"));
    }// Fin try
  
  catch(const Ice::NotRegisteredException&)
    {
      string proxy = communicator()->getProperties()->getProperty("IceGrid.InstanceName") + "/Query";
      IceGrid::QueryPrx query = IceGrid::QueryPrx::checkedCast(communicator()->stringToProxy(proxy));
      startService = StartServicePrx::checkedCast(query->findObjectByType("::FIPA::StartService"));
    }// Fin catch

  // Se comprueba que se tiene un proxy a un objeto del tipo StartService.
  if (!startService)
    {
      cerr << "DirectoryFacilitator --> No se pudo encontrar un objeto ::FIPA::StartService." << endl;
      return;
    }// Fin if

  // DirectoryFacilitator es un servicio básico.
  this->supplyBasicService();

}

void
DirectoryFacilitatorI::
registerAsWKO()
{

  // Registro de DirectoryFacilitator como objeto bien conocido.
  Ice::PropertiesPtr properties = communicator()->getProperties();
  Ice::ObjectAdapterPtr adapter = communicator()->createObjectAdapter("DirectoryFacilitatorAdapter");
  Ice::Identity id = communicator()->stringToIdentity(properties->getProperty("IdentityDF"));

  // Se inicializan los parámetros básicos del servicio.
  this->init(properties->getProperty("InputDF"));
  int i;
  for (i = 0; i < this->getServiceLocator().size(); i++)
    cout << this->getServiceLocator()[i].ServiceSignature << " " << this->getServiceLocator()[i].ServiceAddress << endl;

  adapter->add(this, id);
  adapter->activate();

}

int
DirectoryFacilitatorI::
run(int argc, char *argv[])
{

  try
    {

      // Desde el punto de vista de la implementación, registro de DirectoryFacilitator como objeto bien conocido.
      this->registerAsWKO();
      // DirectoryFacilitator se registra como un servicio básico dentro de la plataforma de agentes.
      this->registerAsBasicService();
      // Suspensión del hilo de ejecución hasta que termina la ejecución del servidor.
      communicator()->waitForShutdown();

      return EXIT_SUCCESS;
    }// Fin try

  catch (const Ice::Exception& ex)
    {
      cerr << ex << " in DirectoryFacilitatorI::run."  <<endl;
      return EXIT_FAILURE;
    }// Fin catch 

}

int
main(int argc, char *argv[])
{

  DirectoryFacilitatorI *dfi = new DirectoryFacilitatorI();
  return dfi->main(argc, argv);
  
}
