#!/bin/sh

echo ""
echo "Script to start MASYRO"
echo ""

# Arrancando el nodo y el registro.
echo "Starting the node and the registry..."
icegridnode --Ice.Config=config/icegrid.cfg --daemon --nochdir
sleep 5
echo "Deploying MASYRO..."

# Desplegando la aplicación
icegridadmin --Ice.Config=config/icegridadmin.cfg -e "application add ./init/MASYRO.xml"
icegridadmin --Ice.Config=config/icegridadmin.cfg -e "server start AMS"
icegridadmin --Ice.Config=config/icegridadmin.cfg -e "server start DirectoryFacilitator"

# Arrancando glacier2router
echo ""
echo "Starting glacier2router"
glacier2router --Ice.Config=config/router.cfg