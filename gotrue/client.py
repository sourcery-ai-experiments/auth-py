import requests
import re
import urllib
import json

HTTPRegexp = "/^http://"
defaultApiURL = "/.netlify/identity"


def jsonify(dictionary: dict):
    return json.dumps(dictionary)


class Client:
    def __init__(self, url, audience='', setCookie=False):
        if re.match(HTTPRegexp, url):
            # TODO: Decide whether to convert this to a logging statement
            print(
                "Warning:\n\nDO NOT USE HTTP IN PRODUCTION FOR GOTRUE EVER!\nGoTrue REQUIRES HTTPS to work securely."
            )
        self.BASE_URL = url

    def settings(self):
        """Get environment settings for the server"""
        return requests.get(f"{self.BASE_URL}/settings")

    def sign_up(self, credentials: dict):
        return requests.post(f"{self.BASE_URL}/signup", jsonify(credentials))

    def sign_in(self, credentials: dict):
        """Sign in with email and password"""
        return self.grant_token("password", credentials)

    def grant_token(self, type: str, data: dict):
        return requests.post(f"{self.BASE_URL}/token?grant_type=#{type}/",
                             jsonify(data))

    def refresh_access_token(self, refresh_token: str):
        return grant_token("refresh_token", {"refresh_token": refresh_token})

    def sign_out(jwt: str):
        """Sign out user using a valid JWT"""
        return requests.post(f"{self.BASE_URL}/logout", auth=jwt)

    def recover(self, email: str):
        """ Send a recovery email """
        data = {"email": email}
        return requests.post(f"{self.BASE_URL}/recover", jsonify(data))

    def get_user(self, jwt: str):
        """Get user info using a valid JWT"""
        return requests.get(f"{self.BASE_URL}/user", auth=jwt)

    def update_user(self, jwt: str, info: dict):
        """Update user info using a valid JWT"""
        return requests.put(f"{self.BASE_URL}/user", auth=jwt, data=info)

    def send_magic_link(self, email: str):
        """Send a magic link for passwordless login"""
        data = json.dumps({"email": email})
        return requests.post(f"{self.BASE_URL}/magiclink", data=data)

    def invite(self, invitation: dict):
        """Invite a new user to join"""
        return requests.post(f"{self.BASE_URL}/invite", jsonify(invitation))