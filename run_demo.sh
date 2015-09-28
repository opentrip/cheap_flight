#!/bin/sh
set -e
VENV_PATH=`pwd`/venv
if [[ ! -d $VENV_PATH ]]; then
    virtualenv $VENV_PATH
    $VENV_PATH/bin/python setup.py install
fi
$VENV_PATH/bin/python cheap_flight/libs/mc.py  # make sure memcached is started on localhost:11211
$VENV_PATH/bin/python demo.py $@
