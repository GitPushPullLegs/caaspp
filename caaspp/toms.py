from caaspp.client import Client

from urllib.parse import quote


class toms(Client):
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
