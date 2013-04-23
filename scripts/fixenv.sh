#!/bin/sh

export DJANGO_SETTINGS_MODULE=mmm.settings
export PYTHONPATH=`dirname $0`/../www/

echo $PYTHONPATH
