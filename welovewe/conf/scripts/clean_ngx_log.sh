#!/bin/bash
# set file path
NGINX_ACCESS_LOG_PATH=/opt/logs/nginx/access/
NGINX_ERROR_LOG_PATH=/opt/logs/nginx/error/

HISTORY_LOG_NAME_PREFIX=log.

# clean 7 days ago log every day
need_delete_access_log=${NGINX_ACCESS_LOG_PATH}${HISTORY_LOG_NAME_PREFIX}$(date -d "7 days ago" +%Y%m%d)
rm -rf ${need_delete_access_log}

need_delete_error_log=${NGINX_ERROR_LOG_PATH}${HISTORY_LOG_NAME_PREFIX}$(date -d "7 days ago" +%Y%m%d)
rm -rf ${need_delete_error_log}