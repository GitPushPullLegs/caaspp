"""A CAASPP automation module.

This module is an attempt to automate many parts of the CAASPP suite of sites in order to gather and submit data efficiently.

TODO:
    Make this login method useful for more than TOMS.
    Create method to select role.
    Define what you want to automate.

"""

import requests
from collections import deque
from urllib.parse import urlsplit
from lxml import etree
import json
import re


class Client:
    _HEADERS = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.77 Safari/537.36"}

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(self._HEADERS)
        self.visit_history = deque(maxlen=10)
        self.session.hooks['response'].append(self._event_hooks)

    def login(self, username: str, password: str, login_code_func):
        """Logs into CAASPP.

        Logs into any CAASPP system since they all use the same authentication.

        Args:
            username: Your CAASPP username.
            password: Your CAASPP password.
            login_code_func: A method that will provide the login code once CAASPP emails it to you.

        Raises:
            ValueError: Invalid credentials.
        """
        self.credentials = dict(username=username, password=password)
        self._login_code_func = login_code_func
        try:
            self.connection_status = self._login()
        except RecursionError:
            return "Recursion Error"


    def _login(self):
        self.session.get("https://mytoms.ets.org/mt/login.htm")
        return self.visit_history[-1].status_code == 200

    def _event_hooks(self, r, *args, **kwargs):
        """Primary purpose is to navigate the authentication process but also tracks visit history and sets self.roles.

        Sets self.roles with the available roles.
        """
        scheme, netloc, path, query, frag = urlsplit(r.url)
        print(r.url, r.status_code)
        if path == "/auth/realms/california/protocol/saml" and r.status_code == 200:
            self.session.cookies.update(r.cookies.get_dict())
            root = etree.fromstring(r.text, parser=etree.HTMLParser(encoding='utf8'))
            submit_link = root.xpath('//*[@id="kc-form-login"]')[0].get('action')
            print("Logging in")
            self.session.post(submit_link, data=self.credentials)
        elif path == "/auth/realms/california/login-actions/authenticate" and r.status_code == 200:
            # The same path is used for incorrect credentials, access code requests, and the javascript warning.
            root = etree.fromstring(r.text, parser=etree.HTMLParser(encoding='utf8'))
            feedback_text = root.xpath('//*[@class="kc-feedback-text"]')
            if feedback_text:  # Logging in still
                if feedback_text[0].text == "A code has been sent to your email address. " \
                                            "The code will expire after 15 minutes.":
                    print("Running login code function")
                    payload = dict(emailcode=self._login_code_func(), login="Submit")
                    submit_link = root.xpath('//*[@id="kc-email-code-login-form"]')[0].get('action')
                    self.session.post(submit_link, data=payload)
                else:
                    raise ValueError("Invalid credentials.")
            else:
                SAML_response = root.xpath('//*[@name="SAMLResponse"]')[0].get('value')
                self.session.post("https://mytoms.ets.org/mt/fedletapplication", data=dict(SAMLResponse=SAML_response))
        elif path == "/mt/fedletapplication":
            print("Successfully authenticated")
        elif path == "/TOMS" and r.status_code == 200:
            if not "selectedProgram=CAASPP" in query:
                root = etree.fromstring(r.text, parser=etree.HTMLParser(encoding='utf8'))
                scripts = root.xpath('//*/script')
                regex_pattern = r"(?<=var caasppInfoString = ['|\"])[\w\W]+}}(?=['|\"];)"
                for script in scripts:
                    try:
                        json_data = re.findall(regex_pattern, script.text)
                        if json_data:
                            data = json_data[0].replace("\\t", "").replace("\\", '').replace("'", '"')
                            json_data = json.loads(data)['info']
                            self.user_id = json_data['userInfo']
                            self.roles = json_data['roleOrgs']
                            break
                    except (IndexError, TypeError):
                        pass
        else:
            self.visit_history.append(r)
            return r
