/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <Ice/Ice.h>
#include <FIPA.h>
#include <Util.h>
#include <cstring>
#include <fstream>
#include <DOMBuilder.hpp>
#include <AbstractDOMParser.hpp>

using namespace std;
using namespace FIPA;

// CLASE ContentRDF
class ContentRDF
{

 public:

  static int createAction(string act, string actor, vector<string> arguments, string &content);
  static int createProposition(string subject, string predicate, string object, string &content);

};
// FIN CLASE ContentRDF
