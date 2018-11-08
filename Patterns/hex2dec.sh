#!/bin/bash
if [ $#  == 1 ]; then
    printf "%d\n" $1
else
    echo 'Incorrect Usage! ./hex2dec <hexcharacter>'
fi
#EOF
