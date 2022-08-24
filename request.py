import datetime
import os
import random
import socket
from typing import Any

import jinja2

PID = os.getpid()
HOSTNAME = socket.gethostname()


def _payload_id() -> str:
    ts = int(datetime.datetime.utcnow().timestamp())
    rnd = random.randint(1, 2**20)
    return f"{ts}.{PID}.{rnd}@{HOSTNAME}"


def _timestamp() -> str:
    return datetime.datetime.utcnow().isoformat(timespec="minutes")


# noinspection HttpUrlsUsage
RequestTemplate = jinja2.Template(
    """<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE cXML SYSTEM "http://xml.cxml.org/schemas/cXML/1.2.014/cXML.dtd">
<cXML{{ {
  'xml:lang': cxml['xml:lang'] | default('en-US'),
  'payload_id': cxml['payload_id'],
  'timestamp': cxml['timestamp']
} | xmlattr }}>
 <Header>{{ header }}</Header>
 <Request>{{ request }}</Request>
</cXML>
"""
)


def render(
    template: jinja2.Template = RequestTemplate,
    payload_id: str = None,
    timestamp: str = None,
    header: Any = None,
    request: Any = None,
):
    cxml = {
        "payload_id": payload_id if payload_id else _payload_id(),
        "timestamp": timestamp if timestamp else _timestamp(),
        "header": header,
        "request": request,
    }
    return template.render(cxml=cxml)
