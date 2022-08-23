import datetime
import os
import random
import socket

import jinja2

HOSTNAME = socket.gethostname()
PID = os.getpid()

def payload_id():
    ts = int(datetime.datetime.utcnow().timestamp())
    rnd = random.randint(1,2**20)
    return f"{ts}.{PID}.{rnd}@{HOSTNAME}"

def timestamp():
    return datetime.datetime.utcnow().isoformat(timespec='minutes')

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
tmpl = env.get_template('request.xml.jinja2').render(payload_id=payload_id(), timestamp=timestamp())

