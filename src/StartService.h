/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fern�ndez *************************/
/************************************************************/

#include <Service.hpp>

using namespace std;
using namespace FIPA;

class StartServiceI : virtual public StartService,
		      public Ice::Application,
		      public Service
{
  
 public:

  StartServiceI();
  ~StartServiceI();

  /******* INTERFAZ P�BLICA DEL SERVICIO STARTSERVICE */
  // getServiceRoot permite conocer cu�les son los servicios b�sicos de la plataforma.
  virtual ::FIPA::TServiceDirectoryEntries getServiceRoot(const ::Ice::Current&) const;
  // supplyBasicService permite a un servicio darse de alta como servicio b�sico de la plataforma.
  virtual void supplyBasicService(const ::FIPA::TServiceDirectoryEntry&, const ::Ice::Current&);
  /******* FIN INTERFAZ P�BLICA DEL SERVICIO STARTSERVICE */

  void registerAsWKO();

  virtual int run(int, char*[]);

 private:

  // ServiceRoot representa la informaci�n necesario para interactuar con un servicio.
  // Es la informaci�n que un agente solicita en su arranque.
  TServiceDirectoryEntries ServiceRoot;
  
};
