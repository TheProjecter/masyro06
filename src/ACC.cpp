/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <ACC.h>

ACCI::
ACCI()
{
}

ACCI::
~ACCI()
{
}

void
ACCI::
send(TAID to, TAID from, string ACLMessage)
{

  AgentPrx agent;
  int address;
  bool delivered = false;

  // El objetivo es entregar el mensaje al agente.
  for (address = 0; address < to.Addresses.size(); address++) {
    
    try
      {

	// Se crea un proxy al agente para enviarle el mensaje a través de su/sus dirección/direcciones de contacto.
	Ice::ObjectPrx proxy = communicator()->stringToProxy(to.Addresses[address]);
	agent = AgentPrx::uncheckedCast(proxy);
	agent->receiveACLMessage(ACLMessage);
      
	cout << "ACC --> Enviando mensaje de " << from.Name << " a " << to.Name << endl;
	delivered = true;

	// Si llega a este punto, el mensaje ha sido entregado.
	break;
      
      }// Fin try
  
    // Si se produjo un fallo al entregar en una dirección de transporte se intenta de nuevo con la siguiente.
    catch (const Ice::Exception& ex)
      {
	cout << "ACC --> Fallo al entregar un mensaje a " << to.Addresses[address] << endl;
      }// Fin catch

  }// Fin for
  
  // Si no se pudo entregar el mensaje se notifica al emisor del mismo.
  //if (!delivered)
  //this->send(from, from, ACLMessage);

}

::Ice::Int
ACCI::
receive(const ::FIPA::TMessage& message, const ::Ice::Current&)
{

  int i;

  cout << "ACC --> Recibiendo un mensaje." << endl;

  // Se envía una copia del mensaje a cada uno de los receptores.
  for (i = 0; i < message.Envelope.To.size(); i++) {
    cout << "ACC --> Enviando un mensaje a " << message.Envelope.To[i].Name  << endl;
    this->send(message.Envelope.To[i], message.Envelope.From, message.Payload);
  }// Fin for

}

int
ACCI::
supplyBasicService()
{
  
  try
    {    
      startService->supplyBasicService(ServiceDirectoryEntry); 
    }// Fin try
 
  catch (const Ice::Exception& ex)
    {
      cerr << ex << " in ACCI::supplyBasicService." << endl;
    }// Fin catch 
 
}

void
ACCI::
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
      cerr << "ACC --> No se pudo encontrar un objeto ::FIPA::StartService." << endl;
      return;
    }// Fin if

  // ACC es un servicio básico.
  this->supplyBasicService();

}

void
ACCI::
registerAsWKO()
{

  // Registro de ACC como objeto bien conocido.
  Ice::PropertiesPtr properties = communicator()->getProperties();
  Ice::ObjectAdapterPtr adapter = communicator()->createObjectAdapter("ACCAdapter");
  Ice::Identity id = communicator()->stringToIdentity(properties->getProperty("IdentityACC"));

  // Se inicializan los parámetros básicos del servicio.
  this->init(properties->getProperty("InputACC"));

  adapter->add(this, id);
  adapter->activate();

}

int
ACCI::
run(int argc, char *argv[])
{

  try
    {
      // Desde el punto de vista de la implementación, registro de ACC como objeto bien conocido.
      this->registerAsWKO();
      // ACC se registra como un servicio básico dentro de la plataforma de agentes.
      this->registerAsBasicService();
      // Suspensión del hilo de ejecución hasta que termina la ejecución del servidor.
      communicator()->waitForShutdown();

      return EXIT_SUCCESS;
    }// Fin try

  catch (const Ice::Exception& ex)
    {
      cerr << ex << "in ACCI::run."  <<endl;
    }// Fin catch 

}

int
main(int argc, char *argv[])
{

  ACCI *acci = new ACCI();
  return acci->main(argc, argv);

}

