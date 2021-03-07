"""An unofficial API for the CAASPP TOMS website.

This under construction module is meant to allow us to upload users, test settings, test assignments to TOMS as well as download data from TOMS.

    Basic setup:

    client = TOMS()
    client.login(username='username', password='password', login_code_func=login_code_func)
    client.set_role(organization_id=12345, role_id=4)
    ...
"""

from caaspp.client import Client

from urllib.parse import quote, urljoin

class TOMS(Client):
    _HOST = "https://mytoms.ets.org/"

    def login(self, username: str, password: str, login_code_func):
        self._login(link=urljoin(self._HOST, r"mt/login.htm"), username=username, password=password, login_code_func=login_code_func)

    def set_role(self, organization_id: int, role_id: int):
        """Set's the user's role in the TOMS system.

        If you do not know what your organization or role IDs are, print the roles variable after you login.

        Args:
             organization_id: The ID for your organization.
             role_id: The role you'd like to assume in that organization.

        Raises:
            ValueError: Invalid organization_id or role_id.
        """
        if not any((role['org_id'] == organization_id and role['role_id'] == role_id) for role in self.roles):
            raise ValueError("Invalid organization_id or role_id.")
        params = dict(selectedRoleId=role_id, selectedOrgId=organization_id, selectedAYC=6, selectedExtended=0,
                      username=quote(self.credentials['username']), userid=self.user_id)
        self.session.get(r"https://mytoms.ets.org/TOMS?selectedProgram=CAASPP", params=params)
