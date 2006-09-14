#ifndef _FIPA
#define _FIPA

module FIPA
{

/************************/
/*Estructuras generales.*/
/************************/

sequence <string> Sstring;

/**************************************************************/
/*Definición de la estructura básica para definir un servicio.*/
/**************************************************************/

// Estructura del tipo TServiceLocationDescription.
struct TServiceLocationDescription
{

	// ServiceSignature indica la firma vinculante a un servicio.
	string ServiceSignature;
	// ServiceAddress indica como unirse a un servicio.
	// Se entiende como la cadena de texto que representa al proxy asociado al objeto que proporciona un servicio,
	// es decir, al objeto bien conocido.
	string ServiceAddress;

};       

// Estructura del tipo TServiceLocator.
// Sirve para acceder y hacer uso de un servicio.
sequence <TServiceLocationDescription> TServiceLocator;

// La estructura TServiceDirectoryEntry es un conjunto de parámetros que definen a un servicio.
struct TServiceDirectoryEntry
{

	// ServiceType define el tipo de servicio.
	string ServiceType;
	TServiceLocator ServiceLocator;
	// ServiceId sirve para identificar un servicio de forma única dentro de la plataforma de agentes.
	string ServiceId;

};

sequence <TServiceDirectoryEntry> TServiceDirectoryEntries;

struct TProperty
{
	// Name representa el nombre de la propiedad.
	string Name;
	// Value representa el nombre de la propiedad.
	string Value;
};

sequence <TProperty> TProperties;

/*********************************************/
/*Descripción del identificador de un agente.*/
/*********************************************/

// El AID es una colección extensible de parámetros que identifican a un agente.
struct TAID
{
	// Name identifica a un agente de manera única en la plataforma de agentes.
	// Es de la forma nombre-agente@plataforma-agentes.
	string Name;
	// Addresses es una lista de direcciones de transporte donde un mensaje puede ser entregado.
	Sstring Addresses;
};

sequence <TAID> TAIDs;

/*********************************************************/
/*Descripción de un agente en el Agent Management System.*/
/*********************************************************/

enum EState {Initiated, Active, Suspended, Waiting, Transit};
enum EExplanation {Duplicate, Access, Invalid, Success, NotFound};

// AMSAgentDescription representa la información por la cual el AMS conoce a los agentes.
struct TAMSAgentDescription
{
	// Name representa el identificador del agente.
	TAID Name;
	//State representa el estado del agente.
	int State;
};

sequence <TAMSAgentDescription> TAgentDirectory;

/********************************************************/
/*Descripción de un servicio en el DirectoryFacilitator.*/
/********************************************************/

struct TDFServiceDescription
{
	// Name representa el nombre del servicio.
	string Name;
	// Type representa el tipo de servicio.
	string Type;
};

sequence <TDFServiceDescription> TDFServiceDescriptions;

/*******************************************************/
/*Descripción de un agente en el Directory Facilitator.*/
/*******************************************************/

struct TDFAgentDescription
{
	// Name es el identificador del agente.
	TAID Name;
	// Services es una lista de servicios soportados por el agente.
	TDFServiceDescriptions Services;
	// Protocols es una lista de protocolos de interacción soportados por el agente.
	Sstring Protocols;
	// Ontologies es una lista de ontologías soportadas por el agente.
	Sstring Ontologies;
	// Languages es una lista de lenguajes de contenido soportados por el agente.
	Sstring Languages;
	// Lease-Time representa el tiempo en segundos que dura el registro del agente.
	int LeaseTime;
	// Scope define la visibilidad de la descripción del agente en el DirectoryFacilitator.
	Sstring Scope;
};

sequence <TDFAgentDescription> TDFAgentDescriptions;

/**********************************************/
/*Elementos de Message Transport Specification*/
/**********************************************/

// Estructura para representar una fecha.
struct TDate
{
	int hour;
	int minutes;
	int seconds;
	int day;
	int month;
	int year;
};

// Estructura para representar el "sobre" del mensaje.
struct TEnvelope
{
	TAIDs To;
	TAID From;
	TDate Date;
	int ACLRepresentation;		
};

// Estructura para representar un mensaje.
struct TMessage
{
	TEnvelope Envelope;
	string Payload;
};

// Representaciones del mensaje ACL.
enum EAclRepresentation {bitefficientRep,
			stringRep,
			xmlRep};

/***************************/
/*Definición de excepciones*/
/***************************/

// Excepción base.
exception BaseException
{
	string Reason;
};

/***************************/
/*Descripción de interfaces.*/
/***************************/

// StartService es el servicio que provee de los servicios básicos a un agente cuando éste comienza su ejecución.
interface StartService
{
	// La operación getBasicServices permite que un agente descubra los servicios básicos.
	// como el AMS, el MTS, o el DF.
	nonmutating TServiceDirectoryEntries getServiceRoot();
	// La operación supplyBasicService permite que un servicio notifique al StartService que es un servico básico	.
	void supplyBasicService(TServiceDirectoryEntry sde);
};

enum Matching {SAME, ANY};

// Agent Management System es el servicio controlador de la plataforma de agentes.
interface AMS
{
	// La operación register permite que un agente se registre en la plataforma de agentes.
	void register(TAID aid, out int explanation, out string newName, out int state);
	// La operación deregister permite que un agente elimine su registro en la plataforma de agentes.
	void deregister(TAID aid, out int explanation);
	// La operación modify permite que un agente modifique sus datos en el AMS.
	idempotent void modify(TAID aid, out int explanation);
	// La operación search permite buscar uno o varios agentes según unos criterios.
	nonmutating void search(TAID aid, int match, out int explanation, out TAIDs aids);
	// La operación getDescription permite obtener la descripción del AP.
	nonmutating string getDescription();
};

enum DFOperation {REGISTER, DEREGISTER, MODIFY};

// Agent representa a un agente en la plataforma de agentes.
interface Agent
{
	// La operación suspend permite suspender la ejecución de un agente.
	idempotent void suspend();
	// La operación terminate permite terminar la ejecución de un agente.
	void terminate();
	// La operación resume permite reanudar la ejecución de un agente.
	idempotent void resume();
	// La operación receiveACLMessage permite recibir un mensaje ACL.
	void receiveACLMessage(string ACLMessage);
};

// DirectoryFacilitator es un servicio de páginas amarillas dentro de la plataforma de agentes.
interface DirectoryFacilitator
{
	// La operación register permite que un agente se registre en el DirectoryFacilitator.
	void register(TDFAgentDescription ad, out int explanation);
	// La operación deregister permite que un agente elimine su registro en el DirectoryFacilitator.
	void deregister(TDFAgentDescription ad, out int explanation);
	// La operación modify permite que un agente modifique sus datos en el DirectoryFacilitator.
	idempotent void modify(TDFAgentDescription ad, out int explanation);
	// La operación search permite buscar uno o varios agentes según unos criterios.
	nonmutating void search(TDFAgentDescription ad, int match, out int explanation, out TDFAgentDescriptions ads);
};

// Agent Communication Channel provee el servicio del Message Transport Service en la plataforma de agentes.
interface ACC
{
	// La operación receive permite recibir un mensaje.
	int receive(TMessage message);
};

};

#endif