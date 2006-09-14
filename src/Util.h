/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#ifndef UTIL
#define UTIL

#include <Ice/Ice.h>
#include <iostream>
#include <FIPA.h>
#include <PlatformUtils.hpp>
#include <XMLString.hpp>
#include <DOM.hpp>
#include <DOMImplementation.hpp>
#include <DOMWriter.hpp>
#include <StdOutFormatTarget.hpp>
#include <LocalFileFormatTarget.hpp>
#include <XercesDOMParser.hpp>
#include <XMLUni.hpp>
#if defined(XERCES_NEW_IOSTREAMS)
#include <iostream>
#else
#include <iostream.h>
#endif
#include <OutOfMemoryException.hpp>

XERCES_CPP_NAMESPACE_USE

using namespace std;
using namespace FIPA;

class Util
{

 public:

  static bool isAgentRegistered(string agentName, TAgentDirectory ad); 
  static bool isAgentRegisteredDF(string agentName, TDFAgentDescriptions ads);
  static bool removeRegisteredAgent(string agent, TAgentDirectory& ad);
  static bool removeRegisteredAgentDF(string agent, TDFAgentDescriptions& ads);
  static bool modifyRegisteredAgent(TAID aid, TAgentDirectory& ad);
  static bool modifyRegisteredAgentDF(TDFAgentDescription ad, TDFAgentDescriptions& ads);
  static bool existService(TServiceDirectoryEntry sde, TServiceDirectoryEntries serviceRoot);
  static bool existsAgentService(string service, TDFAgentDescription ad);
  static bool removeAID(TAID aid, TAgentDirectory& ad);
  static void showAgentNames(TAgentDirectory& ad);

};

class XStr
{
  
 public:
    
  XStr(const char* const toTranscode);
  ~XStr();
  const XMLCh* unicodeForm() const;
  
 private:
  
  XMLCh*   fUnicodeForm;
  
};

#define X(str) XStr(str).unicodeForm()

#endif
