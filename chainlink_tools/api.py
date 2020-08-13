import requests


def process_response(response):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        raise requests.exceptions.HTTPError(
            f"Error encountered:\n{http_error}\n{response.text}"
        )

    try:
        return response.json()
    except ValueError:
        raise requests.exceptions.HTTPError(
            f"Error encountered. Cannot decode JSON response.\n{response.text}"
        )


def get_response_data(response):
    data = response.get("data", response)

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
        response = process_response(response)

        data = get_response_data(response)

        while response.get("links", {}).get("next"):
            path = response["links"]["next"]
            response = self._session.request(method, self._build_url(path), **kwargs)
            response = process_response(response)

            data.extend(get_response_data(response))

        return data

    def _build_url(self, path):
        return f"{self._url}{path}"

    def _login(self, email, password):
        self._request("post", "/sessions", json={"email": email, "password": password})

    def get_specs(self):
        return self._request("get", "/v2/specs")

    def create_spec(self, data):
        return self._request("post", "/v2/specs", json=data)
