import unittest

from credentials import CredentialMac


class TestCredentialMac(unittest.TestCase):
    def test_mac(self):
        credential_mac = CredentialMac(
            creationDate="2003-01-15T08:42:46-08:00",
            expirationDate="2003-01-15T11:42:46-08:00",
        )
        self.assertEqual(credential_mac.mac(), "cR6Jpz58nriXERDN")

    def test_mac_password(self):
        credential_mac = CredentialMac(
            creationDate="2003-01-15T08:42:46-08:00",
            expirationDate="2003-01-15T11:42:46-08:00",
        )
        self.assertEqual(credential_mac.mac("password"), "5KMM/p4KtK5oAf/B")

    def test_xml(self):
        credential_mac = CredentialMac(
            creationDate="2003-01-15T08:42:46-08:00",
            expirationDate="2003-01-15T11:42:46-08:00",
        )
        self.assertEqual(
            credential_mac.xml(),
            '<CredentialMac type="FromSenderCredentials" algorithm="HMAC-SHA1-96" creationDate="2003-01-15T08:42:46-08:00" expirationDate="2003-01-15T11:42:46-08:00">cR6Jpz58nriXERDN</CredentialMac>',
        )


if __name__ == "__main__":
    unittest.main()
