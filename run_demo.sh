#!/bin/sh
set -x
set -e
export PYTHONPATH=`pwd`
python cheapflight/libs/mc.py
python demo.py $@
