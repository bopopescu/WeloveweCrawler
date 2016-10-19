#encoding=utf-8
import time
import datetime

def show_add_time(date_time_str):
    '''
    format date for readability
    '''
    seconds = 0
    date_time_str = date_time_str.strip()
    if date_time_str.isdigit():
        seconds = int(date_time_str)
        if len(date_time_str) == 13:
            seconds = seconds / 1000
        dt = datetime.datetime.fromtimestamp(seconds)
    else:
        if len(date_time_str) == 10:
            fmt = "%Y-%m-%d"
        else:
            fmt = "%Y-%m-%d %H:%M:%S"
        try:
            dt = datetime.datetime.strptime(date_time_str, fmt)
        except Exception:
            return ''
    now = datetime.datetime.now()
    ms = int((now - dt).total_seconds())
    if ms < 120:
        tmp_str = u'刚刚'
    elif ms < 3600:
        tmp_str = str(ms / 60) + u'分钟前'
    elif ms < 86400 and now.day == dt.day:
        tmp_str = u'今天 ' + dt.strftime('%H:%M')
    elif ms < 172800 and now.day == dt.day + 1:
        tmp_str = u'昨天 ' + dt.strftime('%H:%M')
    elif now.year == dt.year:
        tmp_str = dt.strftime('%m-%d %H:%M')
    else:
        tmp_str = dt.strftime('%Y-%m-%d')

    return  tmp_str

def show_create_time(date_str):
    '''
    discard time and format date
    '''
    milliseconds = int(time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M:%S")))
    format_str = u"%Y年%m月%d日".encode('utf-8')
    tmp_str = datetime.datetime.fromtimestamp(milliseconds).strftime(format_str)
    tmp_str = tmp_str.decode('utf-8')
    return  tmp_str

def get_timestamp(date_time_str):
    seconds = 0
    date_time_str = date_time_str.strip()
    if date_time_str.isdigit():
        seconds = int(date_time_str)
        if len(date_time_str) == 13:
            seconds = seconds / 1000
    else:
        if len(date_time_str) == 10:
            fmt = "%Y-%m-%d"
        else:
            fmt = "%Y-%m-%d %H:%M:%S"
        try:
            seconds = time.mktime(time.strptime(date_time_str, fmt))
        except Exception:
            pass

    return seconds

def parse_date(timestamp):
    if not isinstance(timestamp, int):
        try:
            timestamp = int(timestamp)
        except:
            timestamp = int(time.time())
    dt = datetime.date.fromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d'), timestamp / 86400 * 86400

def show_last_modify(timestamp):
    if not isinstance(timestamp, int):
        try:
            timestamp = int(timestamp) / 1000
        except:
            timestamp = int(time.time())
    else:
        timestamp = timestamp / 1000
    dt = datetime.date.fromtimestamp(timestamp)
    return dt.strftime('%Y/%m/%d')

def parse_create_time(date_str):
    '''
    return milliseconds
    '''
    milliseconds = int(time.mktime(time.strptime(date_str,
        "%Y-%m-%d %H:%M:%S"))) * 1000

    return milliseconds

def get_order_time():
    dt = datetime.datetime.now()
    return dt.strftime('%Y%m%d%H%M%S')

def parse_order_time(tmstr):
    return datetime.datetime.strptime(tmstr, '%Y%m%d%H%M%S')
