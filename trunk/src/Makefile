SLICE=/usr/bin
CXXFLAGS=-I. -I../FIPA/generated/ -I/usr/include -I/usr/include/xercesc/dom -I/usr/include/xercesc/util -I/usr/include/xercesc/parsers -I/usr/include/xercesc/framework

LDFLAGS=-L/usr/lib
LDLIBS=-lxerces-c -lIce -IceUtil -lIceGrid -lIceBox -lIceStorm

all: StartService AMS Agent DirectoryFacilitator ACC

FIPA.o: ../FIPA/generated/FIPA.cpp
InputService.o: ../FIPA/generated/FIPA.cpp InputService.cpp Util.cpp
Service.o: ../FIPA/generated/FIPA.cpp InputService.cpp Service.cpp
StartService.o: ../FIPA/generated/FIPA.cpp Service.cpp StartService.cpp
AMS.o: ../FIPA/generated/FIPA.cpp Service.cpp AMS.cpp
DirectoryFacilitator.o: ../FIPA/generated/FIPA.cpp Service.cpp DirectoryFacilitator.cpp
ACC.o: ../FIPA/generated/FIPA.cpp Service.cpp ACC.cpp
ACLMessage.o: ../FIPA/generated/FIPA.cpp ACLMessage.cpp
ContentRDF.o: ContentRDF.cpp
Util.o: ../FIPA/generated/FIPA.cpp Util.cpp
Agent.o: ../FIPA/generated/FIPA.cpp Agent.cpp

StartService: Service.o InputService.o StartService.o ../FIPA/generated/FIPA.o Util.o
AMS: Service.o InputService.o AMS.o ../FIPA/generated/FIPA.o Util.o
ACC: Service.o InputService.o ACC.o ../FIPA/generated/FIPA.o Util.o
DirectoryFacilitator: Service.o InputService.o DirectoryFacilitator.o ../FIPA/generated/FIPA.o Util.o
Agent: Agent.o ../FIPA/generated/FIPA.o ACLMessage.o ContentRDF.o Util.o

../FIPA/generated/%.cpp ../FIPA/generated/%.h: %.ice
	slice2cpp --output-dir ../FIPA/generated $<

clean:
	rm -f *.o Agent StartService ACLMessage ContentRDF AMS ACC DirectoryFacilitator *~
