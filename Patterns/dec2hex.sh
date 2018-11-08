#!/bin/bash
if [ $# == 1 ]; then
    printf "0x%x\n" $1
else
    echo 'Incorrect Usage! ./dec2hex.sh <integer>'
fi
#EOF
