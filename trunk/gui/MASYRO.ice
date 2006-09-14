#ifndef _MASYRO
#define _MASYRO

module MASYRO
{

/************************/
/*Estructuras generales.*/
/************************/

// Estructura que define una zona a renderizar.
struct TZone {

	// Identificador de la zona.
	int id;
	// Coordenadas que definen la zona.
	int x1;
	int y1;
	int x2;
	int y2;
	// Desviación estándar del color de la zona.
	float d;
	// Media de color en la zona.
	float m;

};

sequence <TZone> TZones;

enum StateRegister {Done, NotDone, InWork};

// Estructura que define un registro en la arquitectura de pizarra.
struct TRegister {

	// Identificador del trabajo.
	int IdWork;
	// Identificador de la unidad de trabajo (zona de la imagen).
	int WorkUnit;
	int Size;
	// Complejidad del trozo.
	int Comp;
	// Tiempo estimado por el agente tras un render "tipo sello" (tiempo empírico).
	int Test;
	// Tiempo final empleado por el agente.
	int Treal;
	// Nombre del agente encargado de la unidad de trabajo.
	string Agent;
	// Variable que indica si se completó la unidad de trabajo.
	StateRegister State;
	// Ibs representa el tamaño de la banda de interpolación.
	int Ibs;
	// Ls representa el número de samples por luz.
	int Ls;
	// Rl representa el nivel de recursión.
	int Rl;

};

sequence <TRegister> TRegisters;

sequence <byte> ByteSeq;
sequence <int> IntSeq;

enum StateRenderAgent {Estimating, Bidding, Rendering, Resting, Finishing};

/***************************/
/*Definición de excepciones*/
/***************************/

// Excepción base.
exception BaseException
{
	string Reason;
};

// Excepción lanzada en caso de que al solicitar un modelo éste no exista.
exception ModelNotExistsException extends BaseException
{
	IntSeq ExistingModels;
};

// Excepción lanzada en caso de que no exista un registro a la hora de actualizarlo.
exception RegisterNotExistsException extends BaseException
{
};

/***************************/
/*Descripción de interfaces.*/
/***************************/

// Analyst es el servicio encargado de llevar a cabo el análisis de la entrada.
interface Analyst
{

	// La operación processWork permite procesar un trabajo asociado a una escena.
	// work representa el flujo de bytes asociado al trabajo.
	// workName es el nombre dado al trabajo.
	// level representa el número de pasadas para llevar a cabo la división de la imagen inicial en trozos.
	// optimization es el nivel de optimización definido por el usuario.
	// void processWork(ByteSeq work, string workName, int level, int optimization);
	void processWork(string work, string workName, int level, int optimization);

};

// RenderAgent es la interfaz a un agente especializado en el render.
interface RenderAgent
{

	// La operación notifyNewWork permite al RenderAgent conocer la existencia de un nuevo trabajo.
	void notifyNewWork(TZones zones, int idWork, int benchmarkValue);
	// La operación notifyZone asigna una lista de zonas del nuevo trabajo al RenderAgent, para que éste haga un estudio previo.
	// optimization ==> Nivel de optimización definido por el usuario (1-5).
	["ami"] void notifyZones(TZones zones, int idWork, int optimization);
	// La operación beginRenderProcess notifica el comienzo del trabajo.
	void beginRenderProcess();
	// La operación render notifica al agente el comienzo del renderizado para la zona idZone del trabajo idWork.
	["ami"] void render(int idWork, int idZone, string agent);
	// La operación getState permite obtener el estado del agente.
	nonmutating StateRenderAgent getState();

};

// Master es el servicio publicador de la existencia de nuevos trabajos en la plataforma.
interface Master
{

	// La operación subscribe permite a un agente especializado en el renderizado subscribirse al Master.
	void subscribe(string agentName, RenderAgent* agent);
	// La operación unsubscribe permite a un agente especializado en el renderizado darse de baja con el Master.
	void unsubscribe(string agentName);

	// La operación notifyNewWork permite al Master conocer la existencia de un nuevo trabajo.	
	// optimization ==> Nivel de optimización definido por el usuario (1-5).
	void notifyNewWork(TZones zones, int idWork, int optimization);
	// La operación benchmarkValue incrementa el valor medio del tiempo empleado en la ejecución del benchmark.
	void benchmarkValue(int value);

	// La operación bidHigher permite a un agente pujar por un trozo.
	["ami"] void bidHigher(string agent, int idWork, int idZone, int credits, IntSeq historic);
	// La operación noMoreBiddings le indica al Master la posible finalización del trabajo.
	void noMoreBiddings();
	// La operación giveFinalImage le proporciona al Master un trozo de la imagen final.
	void giveFinalImage(int idWork, int idZone, ByteSeq partialImage, int x1, int y1, int x2, int y2, int ibs);

	// La operación showAgentsState devuelve el estado de todos los agentes.
	nonmutating string showAgentStates();
	// La operación getLog devuelve el log del Master.
	nonmutating string getLog();
	// La operación getFinalTimes devuelve los tiempos finales empleados en un trabajo.
	nonmutating string getFinalTimes();

};

// ModelRepository es la interfaz relativa al almacenamiento/recuperación de modelos.
interface ModelRepository
{

	// put devuelve el identificador asignado al modelo enviado.
	int put(string name, ByteSeq model);
	// get devuelve el nombre del modelo y el propio modelo como secuencia de bytes.
	nonmutating string get(int idModel, out ByteSeq model) throws ModelNotExistsException;

};

// Blackboard es la interfaz relativa a la arquitectura de pizarra.
interface Blackboard
{

	// write escribe un registro en la pizarra.
	void write(TRegister register);
	// read lee un registro de la pizarra, identificado por el id del trabajo y el id de la zona.
	TRegister read(int idWork, int workUnit) throws RegisterNotExistsException;
	// update actualiza el valor de un registro en la pizarra.
	void update(int idWork, int workUnit, int test) throws RegisterNotExistsException;
	// clear limpia la pizarra.
	void clear();

	// setAnalysisTime establece el tiempo empleado para el análisis de la escena más reciente.
	void setAnalysisTime(int time);
	// getAnalysisTime devuelve el tiempo empleado para el análisis de la escena más reciente.
	nonmutating int getAnalysisTime();
	// incrementEstimatedRenderTime incrementa el tiempo de estimación de la escena.
	void incrementEstimatedRenderTime(int time);
	// getEstimatedRenderTime devuelve el tiempo de estimación de la escena.
	nonmutating int getEstimatedRenderTime();

	// isWorkEstimated indica si las distintas partes del trabajo se han estimado.
	bool isWorkPartiallyEstimated();
	// isEnd indica si el trabajo actual ha terminado.
	bool isCurrentWorkFinished();
	// show muestra el contenido de la pizarra.
	string show();
	// getMaxTest devuelve el valor del trozo cuyo tiempo estimado es el mayor del trabajo idWork.
	int getMaxTest(int idWork);
	// getMaxComp devuelve el valor del trozo cuya complejidad es la mayor del trabajo idWork
	int getMaxComp(int idWork);

	// setWorkUnit permite a un agente hacerse cargo de una unidad de trabajo.
	void setWorkUnit(int idWork, int workUnit, string agent) throws RegisterNotExistsException;
	// finishWork permite a un agente notificar la finalización de una unidad de trabajo.
	void finishWorkUnit(int idWork, int workUnit, int treal, int ibs, int ls, int rl) throws RegisterNotExistsException;

};

};

#endif