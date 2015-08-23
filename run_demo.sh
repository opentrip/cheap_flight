#!/bin/sh
set -e
VENV_PATH=`pwd`/venv
if [[ ! -d $VENV_PATH ]]; then
    virtualenv $VENV_PATH
    $VENV_PATH/bin/python setup.py install
fi
$VENV_PATH/bin/python cheap_flight/libs/mc.py  # make sure memcached is started on localhost:11211
$VENV_PATH/bin/python demo.py PEK KUL 2016-04-27 2016-05-08
$VENV_PATH/bin/python demo.py PEK MNL 2015-10-27 2015-11-05
$VENV_PATH/bin/python demo.py MNL PEK 2015-10-27 2015-11-05
