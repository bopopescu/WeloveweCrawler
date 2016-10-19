#!/bin/bash
# set file path
TORNADO_LOG_PATH=/opt/logs/tornado/livecollectportalpy/

# clean 7 days ago log every day
need_delete_log=${TORNADO_LOG_PATH}$(date -d "7 days ago" +%Y%m%d)
rm -rf ${need_delete_log}
