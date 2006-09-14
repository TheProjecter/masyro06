/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#ifndef AGENT
#define AGENT

#include <Ice/Ice.h>
#include <Ice/IdentityUtil.h>
#include <IceGrid/Admin.h>
#include <IceUtil/UUID.h>
#include <IceGrid/Query.h>
#include <IceStorm/IceStorm.h>
#include <FIPA.h>
#include <ACLMessage.h>
#include <ContentRDF.h>
#include <cstring>
#include <fstream>
#include <DOMBuilder.hpp>
#include <AbstractDOMParser.hpp>

using namespace std;
using namespace FIPA;

/*CLASE AgentI*/
class AgentI : virtual public Agent,
	      public Ice::Application
{

 public:

  AgentI(string name);
  ~AgentI();

  TServiceDirectoryEntries getServiceRoot() const;

  // Funcionalidad relativa a los cambios de estado del agente.
  virtual void suspend(const ::Ice::Current&);
  virtual void terminate(const ::Ice::Current&);
  virtual void resume(const ::Ice::Current&);

  // Funcionalidad relativa a la notificación de eventos.
  virtual void notify(const ::FIPA::TDFAgentDescription&, ::Ice::Int, const ::Ice::Current&);

  // Funcionalidad relativa a la gestión del agente.
  void _cpp_register(int& explanation, int&state);
  void deregister(int& explanation);
  void modify(TAID aid, int& explanation);
  void modifyDF(TDFAgentDescription ad, int& explanation);
  void setName(string name);
  string getName();
  void setState(int state);
  int getState();
  TAID getAgentIdentifier();
  void setNameAgentDescription(string name);
  void obtainServiceRoot();
  void setContactAddress(Ice::ObjectAdapterPtr& adapter);
  void addAddress(string address);
  void removeAddress(string address);
  TDFAgentDescription getAgentDescription();
  TDFServiceDescriptions getServices();
  void addService(string name, string type);
  std::vector<string> getProtocols();
  void addProtocol(string protocol);
  void removeProtocol(string protocol);
  void getBasicServiceAMS(int i);
  void getBasicServiceDF(IceStorm::TopicPrx& topic, Ice::ObjectPrx& proxy, Ice::ObjectAdapterPtr& adapter, int i);
  void getBasicServiceACC(Ice::ObjectAdapterPtr& adapter, int i);
  void subscribeDF(IceStorm::TopicPrx& topic, Ice::ObjectPrx& proxy, Ice::ObjectAdapterPtr& adapter);
  void unsubscribeDF(IceStorm::TopicPrx& topic, Ice::ObjectPrx& proxy);
  void getBasicServices(IceStorm::TopicPrx& topic, Ice::ObjectPrx& proxy, Ice::ObjectAdapterPtr& adapter);

  // Funcionalidad relativa al envío/recepción de mensajes ACL.
  void send(string performative, TAIDs to, int ACLRepresentation, string payload, string language, string protocol, string idConv);
  void send(TMessage message);
  virtual void receiveACLMessage(const ::std::string& message, const ::Ice::Current&);

  virtual int run(int, char*[]);

 private:

  // AgentIdentifier representa la información que identifica a un agente.
  TAID AgentIdentifier;
  // State representa el estado de un agente.
  // Initiated, Active, Suspended, Waiting, Transit.
  int State;
  // ServiceRoot representa la información de los servicios básicos de la plataforma MASYRO.
  TServiceDirectoryEntries ServiceRoot;
  // AgentDescription representa la información del agente en el DirectoryFacilitator.
  TDFAgentDescription AgentDescription;
  // AgentDescriptions representa la información de los agentes registrados en el DirectoryFacilitator.
  TDFAgentDescriptions AgentDescriptions;
  // startService es un proxy al servicio StartService
  StartServicePrx startService;
  // ams es un proxy al servicio AMS
  AMSPrx ams;
  // df es un proxy al servicio DirectoryFacilitator
  DirectoryFacilitatorPrx df;
  // acc es un proxy al servicio ACC
  ACCPrx acc;

};
/*FIN CLASE AgentI*/

#endif
