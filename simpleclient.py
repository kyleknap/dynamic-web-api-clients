import json

import requests


class Client(object):
    def __init__(self, endpoint_url):
        """A JSON RPC client

        :type endpoint_url: str
        :param endpoint_url: The endpoint url to send requests to
        """
        self._endpoint_url = endpoint_url
        self._id_count = 0

    def make_api_call(self, method, params):
        """Make a request to the JSON RPC endpoint

        :type method: str
        :param method: The web API method to make a request to.

        :type params: list or dict
        :param params: A dumped JSON document representing the parameters to
            send to the API method.
        """
        # Set the headers.
        headers = {'content-type': 'application/json'}
        # Set the payload.
        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': self._id_count
        }
        self._id_count += 1
        # Make a post against the endpoint.
        return requests.post(
            self._endpoint_url, data=json.dumps(payload),
            headers=headers).json()
