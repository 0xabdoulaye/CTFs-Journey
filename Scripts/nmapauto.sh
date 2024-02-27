#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'  # No Color

if [ -z "$1" ]; then
    echo -e "${RED}Usage: $0 <IP>${NC}"
    exit 1
fi

target="$1"
TMP_FILE="/tmp/nmap_output_$((RANDOM % (10000000000 - 1000000000 + 1) + 1000000000))" # creating a random file in /tmp for later use
resultat=$TMP_FILE

echo -e "\n${GREEN}###############################################"
echo -e "###---------) Starting Quick Scan (---------###"
echo -e "###############################################${NC}\n"

nmap $target -v 2>&1 | tee $resultat
ports=$(cat $resultat | grep '^[0-9]' | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//)
echo -e "\n\n${GREEN}----------------------------------------------------------------------------------------------------------"
echo "Open Ports : $ports"
echo -e "----------------------------------------------------------------------------------------------------------${NC}\n\n"

rm $resultat   
export Ports=$ports

nmap -sV -Pn -p- -T4 --min-rate=1500 $target -v 2>&1 | tee $resultat
ports=$(cat $resultat | grep '^[0-9]' | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//)

echo -e "\n\n${GREEN}----------------------------------------------------------------------------------------------------------"
echo "Open Ports : $ports"
echo -e "----------------------------------------------------------------------------------------------------------${NC}\n\n"

rm $resultat   
export Ports=$ports

echo -e "\n${GREEN}###############################################"
echo -e "###---------) Starting Second Scan (---------###"
echo -e "###############################################${NC}\n"

nmap $target -sV -sC -Pn -p$ports -v 2>&1 | tee $resultat
