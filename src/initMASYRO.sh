#!/bin/sh

echo ""
echo "Script to automate the MASYRO deployment"
echo ""

# Compilaci�n del c�digo fuente.
slice2cpp --output-dir ../FIPA/generated/ ../FIPA/FIPA.ice
make clean
echo ""
echo "Compiling the source code..."
make
echo ""