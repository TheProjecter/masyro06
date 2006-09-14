/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <AMS.h>

AMSI::
AMSI()
{

  NumberOfAgents = 0;
  CurrentNumberOfAgents = 0;
      
}

AMSI::
~AMSI()
{
}

void
AMSI::
_cpp_register(const ::FIPA::TAID& aid, ::Ice::Int& explanation, ::std::string& newName, ::Ice::Int& state, const ::Ice::Current&)
{

  TAMSAgentDescription ad;
  std::stringstream aux;

  // Se comprueba si ya existe un agente registrado con el mismo nombre (parámetro Name).
  if (Util::isAgentRegistered(aid.Name, AgentDirectory)) {
    explanation = Duplicate;
    cout << "AMS --> El agente " << aid.Name << " ya existe." << endl;
  }// Fin if

  else {      

    // Registro de un agente que solicita una identidad.
    this->incrementNumberOfAgents();
    this->incrementCurrentNumberOfAgents();
    aux << this->getNumberOfAgents();
    if (aid.Name == "unknown")
      newName = "Agent" + aux.str();

    // Se registra el nuevo agente y se da de alta junto al resto de agentes.
    cout << "AMS --> Registro del agente: " << aid.Name << endl;
    cout << "AMS --> Número actual de agentes en la plataforma: " << this->getCurrentNumberOfAgents() << endl;
    ad.Name = aid;
    ad.State = Initiated;
    state = Initiated;
    AgentDirectory.push_back(ad);      
    explanation = Success;

  }// Fin else

}

void
AMSI::
deregister(const ::FIPA::TAID& aid, ::Ice::Int& explanation, const ::Ice::Current&)
{

  // Se comprueba si el agente estaba registrado en la plataforma MASYRO.
  if (!Util::removeRegisteredAgent(aid.Name, AgentDirectory)) {
    explanation = NotFound;
    cout << "AMS --> El agente " << aid.Name << " no está registrado." << endl;
  }// Fin if
  else {
    cout << "AMS --> El agente " << aid.Name << " elimina su registro." << endl;
    explanation = Success;
    this->decrementCurrentNumberOfAgents();
    cout << "AMS --> Número actual de agentes en la plataforma: " << this->getCurrentNumberOfAgents() << endl;
  }// Fin else

}

void
AMSI::
modify(const ::FIPA::TAID& aid, ::Ice::Int& explanation, const ::Ice::Current&)
{

  // Se comprueba que el aid está en el registro.
  if (!Util::isAgentRegistered(aid.Name, AgentDirectory)) {
    cout << "AMS --> El agente " << aid.Name << " no está registrado." << endl;
    explanation = NotFound;
  }// Fin if
  else  
    if (!Util::modifyRegisteredAgent(aid, AgentDirectory)) {
      cout << "AMS --> No puedo modificar datos del agente " << aid.Name << endl;
      explanation = Invalid;
    }// Fin if
    else
      explanation = Success;
  
}

void
AMSI::
search(const ::FIPA::TAID& aid, ::Ice::Int match, ::Ice::Int& explanation, ::FIPA::TAIDs& aids, const ::Ice::Current&) const
{

  int i;

  switch (match) {

    // Matching total.
  case SAME:
    // Se recorre el AgentDirectory para ver si existe un agente con el nombre proporcionado.
    for (i = 0; i < AgentDirectory.size(); i++)
      if (aid.Name == AgentDirectory[i].Name.Name)
	aids.push_back(AgentDirectory[i].Name);
    break;

    // Matching parcial.
  case ANY:
    // PENDIENTE
    break;

  }// Fin switch

  if (aids.size() == 0)
    explanation = NotFound;
  else
    explanation = Success;

}

::std::string
AMSI::
getDescription(const ::Ice::Current&) const
{

  //return this->getServiceDescription();
  return "";

}

void
AMSI::
supplyBasicService()
{
  
  try
    {
      // AMS proporciona a StartService la información necesaria como servicio gestor de la plataforma de agentes.
      startService->supplyBasicService(ServiceDirectoryEntry);
    }// Fin try
  catch (const Ice::Exception& ex)
    {
      cerr << ex << " int AMSI::supplyBasicService." << endl;
    }// Fin catch
  
}

void
AMSI::
suspendAgent(TAID aid)
{
  // PENDIENTE
}

void
AMSI::
terminateAgent(TAID aid)
{

  AgentPrx agent;

  try
    {

      // Se crea un proxy al agente para notificar su finalización.
      Ice::ObjectPrx proxy = communicator()->stringToProxy(aid.Addresses[0]);
      agent = AgentPrx::checkedCast(proxy);
      agent->terminate();
      
      // El AMS elimina el registro del agente que finaliza su ejecución.
      Util::removeAID(aid, AgentDirectory);
      
      cout << "AMS --> El agente " << aid.Name << " termina su ejecución." << endl;
      
    }// Fin try
  
  catch (const Ice::Exception& ex)
    {
      cerr << ex << " in AMSI::terminateAgent." << endl;
    }// Fin catch
  
}

void
AMSI::
resumeAgent(TAID aid)
{
  // PENDIENTE
}

void
AMSI::
incrementNumberOfAgents()
{

  NumberOfAgents++;

}

int
AMSI::
getNumberOfAgents()
{

  return NumberOfAgents;

}

void
AMSI::
incrementCurrentNumberOfAgents()
{

  CurrentNumberOfAgents++;

}

void
AMSI::
decrementCurrentNumberOfAgents()
{

  CurrentNumberOfAgents--;

}

int
AMSI::
getCurrentNumberOfAgents()
{

  return CurrentNumberOfAgents;

}

void
AMSI::
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
      cerr << "AMS --> No se pudo encontrar un objeto ::FIPA::StartService." << endl;
      return;
    }// Fin if

  // Una vez que tenemos un proxy al servicio StartService, AMS le notifica que es un servicio básico.
  this->supplyBasicService();

}

void
AMSI::
registerAsWKO()
{

  // Registro de AMS como objeto bien conocido.
  Ice::PropertiesPtr properties = communicator()->getProperties();
  Ice::ObjectAdapterPtr adapter = communicator()->createObjectAdapter("AMSAdapter");
  Ice::Identity id = communicator()->stringToIdentity(properties->getProperty("IdentityAMS"));

  // Se inicializan los parámetros básicos del servicio.
  this->init(properties->getProperty("InputAMS"));

  adapter->add(this, id);
  adapter->activate();

}

int
AMSI::
run(int argc, char *argv[])
{

  try
    {

      // Desde el punto de vista de la implementación, registro de AMS como objeto bien conocido.
      this->registerAsWKO();
      // AMS se registra como un servicio básico dentro de la plataforma de agentes.
      this->registerAsBasicService();
      // Suspensión del hilo de ejecución hasta que termina la ejecución del servidor.
      communicator()->waitForShutdown();

      return EXIT_SUCCESS;
    }// Fin try

  catch (const Ice::Exception& ex)
    {
      cerr << ex << "in AMSI::run."  <<endl;
    }// Fin catch 

}

int
main(int argc, char *argv[])
{

  AMSI *amsi = new AMSI;
  return amsi->main(argc, argv);

}
