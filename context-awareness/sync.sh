#!/bin/bash

while [ 1 ]
do
    time rsync -av -e ssh --partial /home/jonathan/wearables/compression/full/ jonathan@172.29.84.39:/home/jonathan/rsync_test
    if [ "$?" = "0" ] ; then
        echo "rsync completed normally"
        exit
    else
        echo "Rsync failure. Backing off and retrying..."
    fi
done
