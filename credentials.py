import base64
import contextlib
import ctypes
import datetime
import hmac
import operator

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


def get_hmac_values(
        obj,
        parts=(
                "fromDomain",
                "fromIdentity",
                "senderDomain",
                "senderIdentity",
                "creationDate",
                "expirationDate",
        ),
) -> bytes:
    for value in operator.attrgetter(*parts)(obj):
        yield ctypes.create_string_buffer(value.encode("utf8"))


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

    # noinspection PyMethodParameters
    @pydantic.validator("*")
    def lower_if_not_date(cls, v, field):
        if field.name.endswith("Date"):
            return v
        return v.lower()

    # noinspection PyMethodParameters
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
        digest = hmac.digest(password, b"".join(get_hmac_values(self)), 'sha1')
        return base64.b64encode(digest[0:12]).decode("utf8")

    def xml(
        self,
        template: jinja2.Template = CredentialMacTemplate,
    ):
        return template.render(credential_mac=self)
