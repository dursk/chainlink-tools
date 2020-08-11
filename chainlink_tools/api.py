import requests


def process_response(response):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        raise requests.exceptions.HTTPError(
            f"Error encountered:\n{http_error}\n{response.text}"
        )

    try:
        response_data = response.json()
    except ValueError:
        return response.text

    data = response_data.get("data", response_data)

    if isinstance(data, list):
        return [d["attributes"] if "attributes" in d else d for d in data]
    else:
        return data


class Chainlink:
    def __init__(self, url, email, password):
        self._session = requests.Session()
        self._url = url

        self._login(email, password)

    def _request(self, method, path, **kwargs):
        response = self._session.request(method, self._build_url(path), **kwargs)
        return process_response(response)

    def _build_url(self, path):
        version = "" if path == "/sessions" else "/v2"

        return f"{self._url}{version}{path}"

    def _login(self, email, password):
        self._request("post", "/sessions", json={"email": email, "password": password})

    def get_specs(self):
        return self._request("get", "/specs")

    def create_spec(self, data):
        return self._request("post", "/specs", json=data)
