import requests

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Chainlink:
    def __init__(self, url, email, password):
        self._session = requests.Session()
        self._email = email
        self._password = password
        self._url = url
        self._login()

    def _request(self, method, path, data_or_params=None):
        kwargs = {"verify": False}

        if method == "get":
            kwargs["params"] = data_or_params
        else:
            kwargs["json"] = data_or_params

        response = self._session.request(method, self._build_url(path), **kwargs)

        response.raise_for_status()

        try:
            response_data = response.json()
        except ValueError:
            return response.text

        try:
            data = response_data["data"]
        except KeyError:
            data = response_data

        if isinstance(data, list):
            return [d["attributes"] if "attributes" in d else d for d in data]
        else:
            return data

    def _build_url(self, path):
        if path == "/sessions":
            return f"{self._url}/sessions"
        else:
            return f"{self._url}/v2{path}"

    def _login(self):
        self._request(
            "post", "/sessions", {"email": self._email, "password": self._password}
        )

    def get_specs(self):
        return self._request("get", "/specs")

    def create_spec(self, data):
        return self._request("post", "/specs", data)
