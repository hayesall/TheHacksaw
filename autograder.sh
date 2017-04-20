#!/bin/bash

# BoostSRL-AutoGrader v0.01
# Written by Alexander L. Hayes
# hayesall@indiana.edu
# Last updated: 4/20/2017

RED='\033[0;31m'
LIGHTGREEN='\033[1;32m'
YELLOW='\033[1;33m'
LIGHTBLUE='\033[1;34m'
NC='\033[0m'
BOLD='\e[1m'
ITAL='\e[3m'
UNDL='\e[4m'

# It will be pretty straightforward to establish that testing is consistent. Training is more difficult.

# Sample call:
# $ bash autograder.sh [JAR-FILE]

function name {
    printf "${BOLD}NAME${NC}\n"
    printf "       autograder - AutoGrader: check for consistency between versions of BoostSRL.\n\n"
}

function synopsis {
    printf "${BOLD}SYNOPSIS${NC}\n"
    printf "       bash autograder.sh [${UNDL}OPTIONS${NC}]... [${UNDL}JAR${NC}]\n\n"
}

function hlp {
    name; synopsis;
}

if [[ ! -z $1 ]]; then
    JAR=$1
    echo $JAR
    exit 0
else
    hlp
    exit 2
fi
