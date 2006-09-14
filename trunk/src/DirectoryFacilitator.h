/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <IceGrid/Query.h>
#include <IceGrid/Admin.h>
#include <IceStorm/IceStorm.h>
#include <IceBox/IceBox.h>
#include <Service.hpp>

using namespace std;
using namespace FIPA;

class DirectoryFacilitatorI : virtual public DirectoryFacilitator,
			      public Ice::Application,
			      public Service
{

 public:
  
  DirectoryFacilitatorI();
  ~DirectoryFacilitatorI();

  /******* INTERFAZ PÚBLICA DEL SERVICIO DIRECTORYFACILITATOR */
  // _cpp_ register permite registrar un agente en el directory facilitator.
  virtual void _cpp_register(const ::FIPA::TDFAgentDescription&, ::Ice::Int&, const ::Ice::Current&);  
  // deregister permite dar de baja a un agente en el directory facilitator.
  virtual void deregister(const ::FIPA::TDFAgentDescription&, ::Ice::Int&, const ::Ice::Current&);
  // modify permite modificar los datos de un agente en el directory facilitator.
  virtual void modify(const ::FIPA::TDFAgentDescription&, ::Ice::Int&, const ::Ice::Current&);
  // search permite buscar un agente con unas determinadas características.
  virtual void search(const ::FIPA::TDFAgentDescription&, ::Ice::Int, ::Ice::Int&, ::FIPA::TDFAgentDescriptions&, const ::Ice::Current&) const;
  /******* FIN INTERFAZ PÚBLICA DEL SERVICIO DIRECTORYFACILITATOR */
  
  int supplyBasicService();
  
  void registerAsBasicService();
  void registerAsWKO();
  void registerAsPublisher();
  
  virtual int run(int, char*[]);
  
 private:
  
  // AgentDirectory representa la información en el DirectoryFacilitator de los agentes en la plataforma MASYRO.
  TDFAgentDescriptions AgentDirectory;
  
  // startService es un proxy al servicio startService.
  StartServicePrx startService;
  
};
