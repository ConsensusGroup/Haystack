#!/bin/sh
#This Module initiates the Node so that the messanger app can be connected to the Tangle
iri=$1
IOTA_NODE=$2
cd $IOTA_Node
java -jar $iri -p 14265
