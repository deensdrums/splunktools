import json
import logging

from splunk.persistconn.application import PersistentServerConnectionApplication
from splunk.rest import simpleRequest

logger = logging.getLogger(__name__)

class HelloWorld(PersistentServerConnectionApplication):

    def __init__(self, _command_line, _command_arg):
        logging.basicConfig(level=logging.INFO)
        super(PersistentServerConnectionApplication, self).__init__()

    def handle(self, in_string):
        """
        Called for a simple synchronous request.
        @param in_string: request data passed in
        @rtype: string or dict
        @return: String to return in response.  If a dict was passed in,
                 it will automatically be JSON encoded before being returned.
        """

        try:
            in_dict = json.loads(in_string.decode('utf-8'))
            authtoken = in_dict["session"]["authtoken"]
        except Exception as e:
            logger.error(f"Error decoding JSON or extracting authtoken: {e}")
            return {'payload': {'error': 'Internal server error'}, 'status': 500}

        try:
            assert in_dict["query"][0][0] == "name"
            name = in_dict["query"][0][1]
        except Exception as e:
            logger.error(f"Unable to find name in query: {e}")
            return {'payload': {'error': 'Unable to find name in query'}, 'status': 400}

        endpoint = "/services/saved/searches"

        try:
            response, content = simpleRequest(path=endpoint, sessionKey=authtoken, method="GET")
        except Exception as e:
            logger.error(f"Error making request to {endpoint}: {e}")
            return {'payload': {'error': 'Internal server error'}, 'status': 500}

        text = "Hello, {}!".format(name)
        payload = {
            "text": text
        }

        return {'payload': payload, 'status': 200}

    def handleStream(self, handle, in_string):
        """
        For future use
        """
        raise NotImplementedError(
            "PersistentServerConnectionApplication.handleStream")

    def done(self):
        """
        Virtual method which can be optionally overridden to receive a
        callback after the request completes.
        """
        pass
