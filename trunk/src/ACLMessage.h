/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#ifndef ACLMESSAGE
#define ACLMESSAGE

#include <FIPA.h>
#include <Util.h>
#include <cstring>
#include <fstream>
#include <DOMBuilder.hpp>
#include <AbstractDOMParser.hpp>

using namespace std;
using namespace FIPA;

// CLASE ACLMessage
class ACLMessage
{

 public:
  
  ACLMessage(string performative, TAIDs to, TAID from, int aclRepresentation, string language, string content, string protocol, string idConv);
  ~ACLMessage();
  
  int createFIPAACLMessage(string &mensaje);
  int createFIPAACLMessageBitEfficient(string &mensaje);
  int createFIPAACLMessageString(string &mensaje);
  int createFIPAACLMessageXML(string &mensaje);
  
  string getPerformative();
  TAIDs getTo();
  TAID getFrom();
  int getACLRepresentation();
  string getLanguage();
  string getContent();
  string getProtocol();
  string getIDConv();
  
 private:
  
  string Performative;
  TAIDs To;
  TAID From;
  int ACLRepresentation;
  string Language;
  string Content;
  string Protocol;
  string IDConv;
  
};
// FIN CLASE ACLMessage

#endif
