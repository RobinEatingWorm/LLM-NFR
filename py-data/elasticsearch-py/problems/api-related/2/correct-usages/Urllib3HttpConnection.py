import logging
import time
import requests
import json

from .exceptions import TransportError, HTTP_EXCEPTIONS, ConnectionError

class RequestsHttpConnection(Connection):
    def pattern(self, method, url, params=None, body=None, timeout=None, **kwargs):
        # ...
        
        self.session = requests.session()
        url = self.host + self.url_prefix + url
        request = requests.Request(method, url, params=params or {}, data=body).prepare()

        response = self.session.send(request, timeout=timeout or self.timeout)
        

  
