import os
import requests
from mitmproxy import ctx, http

class CombinedTX:
    NTS_HOSTNAME = "terminologieserver.nl"

    def __init__(self):
        # Cache the token for calls to the NTS
        self._nts_token = None

    def request(self, flow):
        # Intercepts requests to the Nationale Terminologieserver
        if flow.request.pretty_host == self.NTS_HOSTNAME:
            if not self._nts_token:
                self._refreshNTSToken()

            if self._nts_token:
                # Add authentication header to the request
                flow.request.headers["Authorization"] = "Bearer " + self._nts_token
                ctx.log.info(f"Added NTS auth token to {flow.request.method} {flow.request.pretty_url}")
            else:
                ctx.log.error("No NTS token available")
                flow.response = http.Response.make(401, "No NTS authentication token available")

    def _refreshNTSToken(self):
        """ Retrieve an access token to perform NTS operations and set it to self._nts_token.
            Return True if a token can be retrieved, or False if not. """

        try:
            _nts_user = os.environ["NTS_USER"]
            _nts_pass = os.environ["NTS_PASS"]
        except:
            ctx.log.info("Environment variables NTS_USER and NTS_PASS should be set to support the Nationale Terminologieserver")
            return False

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        body = {
            "username"     : _nts_user,
            "password"     : _nts_pass,
            "client_id"    : "cli_client",
            "client_secret": "",
            "grant_type"   : "password"
        }
        response = requests.post("https://terminologieserver.nl/auth/realms/nictiz/protocol/openid-connect/token",
            headers = headers, data = body)
        if response.status_code == requests.codes.ok:
            ctx.log.info("Got an NTS access token")
            self._nts_token = response.json()["access_token"]
            return True

        ctx.log.info("No authorization")
        self._nts_token = None
        return False

addons = [CombinedTX()]