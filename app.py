import base64
import ctypes
import datetime
import hashlib
import hmac
import os
import random
import socket
import struct

import importlib_resources
import jinja2
import pydantic

import request
from credentials import CredentialMac

a = importlib_resources.files("templates")
print(a.name)

ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(importlib_resources.files("templates")._paths[0])
)

print(request.render())
print(request.render(ENV.get_template("request.xml.jinja2")))

credential_mac = CredentialMac(
    creationDate="2003-01-15T08:42:46-08:00", expirationDate="2003-01-15T11:42:46-08:00"
)
print(credential_mac.xml())
print(credential_mac.xml(ENV.get_template("CredentialMac.jinja2")))
