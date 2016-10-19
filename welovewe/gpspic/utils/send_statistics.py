#encoding=utf-8

import socket
import random

from conf import settings

from tornado.iostream import IOStream

def create_stream():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    stream = IOStream(s)
    addr = random.choice(settings.statistic_hosts)
    return stream.connect(addr)

