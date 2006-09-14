#!/bin/sh

echo ""
echo "Script to automate the MASYRO deployment"
echo ""

# Compilación del código fuente.
slice2cpp --output-dir ../FIPA/generated/ ../FIPA/FIPA.ice
make clean
echo ""
echo "Compiling the source code..."
make
echo ""