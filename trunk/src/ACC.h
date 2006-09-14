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

class ACCI : virtual public ACC,
	     public Ice::Application,
	     public Service
{

 public:
  
  ACCI();
  ~ACCI();

  /******* INTERFAZ PÚBLICA DEL SERVICIO ACC */
  // Funciones relacionadas con el envío y recepción de mensajes ACL.
  void send(TAID to, TAID from, string ACLMessage);
  virtual ::Ice::Int receive(const ::FIPA::TMessage& message, const ::Ice::Current&);
  /******* FIN INTERFAZ PÚBLICA DEL SERVICIO ACC */

  int supplyBasicService();

  void registerAsBasicService();
  void registerAsWKO();

  virtual int run(int, char*[]);
  
 private:
  
  // startService es un proxy al servicio startService.
  StartServicePrx startService;
  // agent es un proxy del tipo AgentPrx
  AgentPrx agent;
  
};
