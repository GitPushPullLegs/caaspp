"""An unofficial API for the CAASPP CERS website.

This under construction module is meant to allow us to upload student groups, and download student data from CERS.

    Basic setup:

    client = CERS()
    client.login(username='username', password='password', login_code_func=login_code_func)
    client.set_role(organization_id=12345, role_id=4)
    ...
"""

from caaspp.client import Client

from urllib.parse import quote, urljoin

class CERS(Client):
    _HOST = "https://reporting.smarterbalanced.org/"

    def login(self, username: str, password: str, login_code_func):
        self._login(link="https://login.smarterbalanced.org/sso/saml2/0oa14zrzacExSAFK5357?fromURI=https://login.smarterbalanced.org/home/smarterbalancedassessmentconsortium_cersproduction_1/0oa17s5opaczfbT05357/aln17sbcwtNiV39Uq357", username=username, password=password, login_code_func=login_code_func)
        #TODO: - Test