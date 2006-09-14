/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
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

  /******* INTERFAZ PÚBLICA DEL SERVICIO STARTSERVICE */
  // getServiceRoot permite conocer cuáles son los servicios básicos de la plataforma.
  virtual ::FIPA::TServiceDirectoryEntries getServiceRoot(const ::Ice::Current&) const;
  // supplyBasicService permite a un servicio darse de alta como servicio básico de la plataforma.
  virtual void supplyBasicService(const ::FIPA::TServiceDirectoryEntry&, const ::Ice::Current&);
  /******* FIN INTERFAZ PÚBLICA DEL SERVICIO STARTSERVICE */

  void registerAsWKO();

  virtual int run(int, char*[]);

 private:

  // ServiceRoot representa la información necesario para interactuar con un servicio.
  // Es la información que un agente solicita en su arranque.
  TServiceDirectoryEntries ServiceRoot;
  
};
