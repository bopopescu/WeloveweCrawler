#!/bin/bash

TORNADO_LOG_DIR=/opt/logs/tornado/livecollectportalpy
YESTERDAY_LOG_DIR=$TORNADO_LOG_DIR/`date -d today +%Y%m%d`

mkdir $YESTERDAY_LOG_DIR
mv $TORNADO_LOG_DIR/*.log-`date -d today +%Y%m%d` $YESTERDAY_LOG_DIR/
