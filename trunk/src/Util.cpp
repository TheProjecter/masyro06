/************************************************************/
/**** MASYRO: A MultiAgent SYstem for Render Optimization ****/
/**** Autor: David Vallejo Fernández *************************/
/************************************************************/

#include <Util.h>

bool
Util::
isAgentRegistered(string agentName, TAgentDirectory ad)
{

  int i;

  // Se recorre el directorio de descripciones de agentes.
  for (i = 0; i < ad.size(); i++)
    // Se comprueba si ya existe un agente con ese mismo nombre.
    if (ad[i].Name.Name == agentName)
      return true;

  return false;

}

bool
Util::
isAgentRegisteredDF(string agentName, TDFAgentDescriptions ads)
{

  int i;

  // Se recorre el directorio de descripciones de agentes.
  for (i = 0; i < ads.size(); i++)
    // Se comprueba si ya existe un agente con ese mismo nombre.
    if (ads[i].Name.Name == agentName)
      return true;

  return false;

}

bool
Util::
removeRegisteredAgent(string agentName, TAgentDirectory& ad)
{

  int i;
  vector<TAMSAgentDescription>::iterator it;

  for (i = 0; i < ad.size(); i++)
    if (ad[i].Name.Name == agentName) {
      it = ad.begin() + i;
      ad.erase(it);
      return true;
    }// Fin if

  return false;

}

bool
Util::
removeRegisteredAgentDF(string agentName, TDFAgentDescriptions& ads)
{

  int i;
  vector<TDFAgentDescription>::iterator it;

  for (i = 0; i < ads.size(); i++)
    if (ads[i].Name.Name == agentName) {
      it = ads.begin() + i;
      ads.erase(it);
      return true;
    }// Fin if

  return false;


}

bool
Util::
modifyRegisteredAgent(TAID aid, TAgentDirectory& ad)
{

  int i;

  for (i = 0; i < ad.size(); i++)
    if (ad[i].Name.Name == aid.Name) {
      ad[i].Name.Addresses = aid.Addresses;
      return true;
    }// Fin if

  return false;

}

bool
Util::
modifyRegisteredAgentDF(TDFAgentDescription ad, TDFAgentDescriptions& ads)
{

  int i;

  for (i = 0; i < ads.size(); i++)
    if (ads[i].Name.Name == ad.Name.Name) {
      ads[i] = ad;
      return true;
    }// Fin if

  return false;

}

bool
Util::
existService(TServiceDirectoryEntry sde, TServiceDirectoryEntries serviceRoot)
{

  int i;

  for (i = 0; i < serviceRoot.size(); i++)
    if (serviceRoot[i].ServiceId == sde.ServiceId)
      return true;

  return false;

}

bool
Util::
existsAgentService(string service, TDFAgentDescription ad)
{

  int j;

    for (j = 0; j < ad.Services.size(); j++)
      if (ad.Services[j].Type == service)
	return true;

  return false;

}

bool
Util::
removeAID(TAID aid, TAgentDirectory& ad)
{

  TAgentDirectory::iterator it;
  int i;

  for (it = ad.begin(), i = 0; it != ad.end(); it++, i++)
    if (ad[i].Name.Name == aid.Name) {
      ad.erase(it);
      return true;
    }// Fin if

  return false;

}

void
Util::
showAgentNames(TAgentDirectory& ad)
{

  int i;

  cout << "AMS --> Los agentes disponibles son: " << endl;

  for (i = 0; i < ad.size(); i++)
    cout << "\t" << ad[i].Name.Name << endl;

}

XStr::
XStr(const char* const toTranscode)
{

  fUnicodeForm = XMLString::transcode(toTranscode);

}

XStr::
~XStr()
{

  XMLString::release(&fUnicodeForm);

}

const XMLCh*
XStr::
unicodeForm() const
{
  return fUnicodeForm;
}
