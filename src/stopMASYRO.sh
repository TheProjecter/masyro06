#!/bin/sh

echo ""
echo "Script to stop MASYRO"
echo ""

echo ""
echo "Closing the MASYRO application..."
icegridadmin --Ice.Config=config/icegridadmin.cfg -e "application remove MASYRO"
echo "Shutdowning localhost..."
icegridadmin --Ice.Config=config/icegridadmin.cfg -e "node shutdown localhost"