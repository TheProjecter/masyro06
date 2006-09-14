/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <IceGrid/Admin.h>
#include <IceGrid/Query.h>
#include <Service.hpp>

using namespace std;
using namespace FIPA;

class AMSI: virtual public AMS,
	    public Ice::Application,
	    public Service
{

 public:
  
  AMSI();
  ~AMSI();

  /******* INTERFAZ PÚBLICA DEL SERVICIO AMS */
  // _cpp_ register permite registrar un agente en la plataforma.
  virtual void _cpp_register(const ::FIPA::TAID&, ::Ice::Int&, ::std::string&, ::Ice::Int&, const ::Ice::Current&);
  // deregister permite dar de baja a un agente en la plataforma.
  virtual void deregister(const ::FIPA::TAID&, ::Ice::Int&, const ::Ice::Current&);
  // modify permite modificar los datos de un agente en la plataforma.
  virtual void modify(const ::FIPA::TAID&, ::Ice::Int&, const ::Ice::Current&);
  // search permite buscar un agente con unas determinadas características.
  virtual void search(const ::FIPA::TAID&, ::Ice::Int, ::Ice::Int&, ::FIPA::TAIDs&, const ::Ice::Current&) const;
  // getDescription permite obtener la descripción general de la plataforma.
  virtual ::std::string getDescription(const ::Ice::Current&) const;
  /******* FIN INTERFAZ PÚBLICA DEL SERVICIO AMS */

  void supplyBasicService();
  void registerAsBasicService();
  void registerAsWKO();

  void suspendAgent(TAID aid);
  void terminateAgent(TAID aid);
  void resumeAgent(TAID aid);

  void incrementNumberOfAgents();
  int getNumberOfAgents();
  void incrementCurrentNumberOfAgents();
  void decrementCurrentNumberOfAgents();
  int getCurrentNumberOfAgents();

  virtual int run(int, char*[]);

 private:

  // AgentDirectory representa la información de los agentes residentes en la plataforma.
  TAgentDirectory AgentDirectory;
  // NumberOfAgents representa el número de agentes que han pasado por la plataforma.
  int NumberOfAgents;
  // CurrentNumberOfAgents representa el número de agentes que actualmente residen en la plataforma.
  int CurrentNumberOfAgents;

  // startService es un proxy al servicio startService.
  StartServicePrx startService;

};
