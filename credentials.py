import base64
import contextlib
import ctypes
import datetime
import hashlib
import hmac

import jinja2
import pydantic


CredentialMacTemplate = jinja2.Template(
    """<CredentialMac{{ { 
  'type': credential_mac.type | default("FromSenderCredentials"),
  'algorithm': credential_mac.algorithm | default("HMAC-SHA1-96"),
  'creationDate': credential_mac.creationDate,
  'expirationDate': credential_mac.expirationDate,
} | xmlattr }}>{{ credential_mac.mac() }}</CredentialMac>
"""
)


class CredentialMac(pydantic.BaseModel):
    fromDomain: str = "NetworkID"
    fromIdentity: str = "AN9900000100"
    senderDomain: str = "NetworkID"
    senderIdentity: str = "AN9900000100"
    creationDate: str = pydantic.Field(default_factory=datetime.datetime.now)
    expirationDate: str = pydantic.Field(
        default_factory=lambda: datetime.datetime.now() + datetime.timedelta(hours=3)
    )

    class Config:
        anystr_strip_whitespace = True
        frozen = True
        validate_assignment = True
        validate_all = True

    @pydantic.validator("*")
    def lower_if_not_date(cls, v, field):
        if field.name.endswith("Date"):
            return v
        return v.lower()

    @pydantic.validator("creationDate", "expirationDate", pre=True)
    def date_is_iso(cls, v):
        if isinstance(v, str):
            v = datetime.datetime.fromisoformat(v)
        return v.isoformat(timespec="seconds")

    def mac(
        self,
        password: str = "abracadabra",
    ) -> str:
        with contextlib.suppress(AttributeError):
            password = password.encode("utf8")
        digest = hmac.new(password, digestmod=hashlib.sha1)
        for part in (
            self.fromDomain,
            self.fromIdentity,
            self.senderDomain,
            self.senderIdentity,
            self.creationDate,
            self.expirationDate,
        ):
            digest.update(ctypes.create_string_buffer(part.encode("utf8")))
        return base64.b64encode(digest.digest()[0:12]).decode("utf8")

    def xml(
        self,
        template: jinja2.Template = CredentialMacTemplate,
    ):
        return template.render(credential_mac=self)
