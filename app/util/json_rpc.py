import json
from random import randint


class JSONRPCException(Exception):

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return "Creation of JSON-RPC packet failed because: {}".format(
            self.message)

    def __str__(self):
        return "Creation of JSON-RPC packet failed because: {}".format(
            self.message)


class JSONRPCBase:

    # None by default, updated when Result or Error created
    response_id = None
    packet = {
        "jsonrpc": "2.0",        # Default required key/value pair for JSON-RPC
        "id": response_id
    }

    def __repr__(self):
        return "<JSON-RPC object - {}>".format(self.id)


class JSONRPCResult(JSONRPCBase):
    """
    JSON-RPC Result object
    """

    def __init__(self, result, response_id=None):
        """
        Create a JSON-RPC Result object
        Returns nothing on success, otherwise JSONRPCException is raised

        Parameters:
            'id':       REQUIRED, otherwise it will be set to None/NULL
            'result':   Required when creating a JSON-RPC Result object
                            MUST be type dict or str (JSON encoded)
        """
        self.response_id = response_id
        self.packet["id"] = self.response_id
        self.type = "Result"

        if type(result) == dict:
            self.data = result
        elif type(result) == str:
            self.data = json.loads(result)
        else:
            raise JSONRPCException("Unexpected data type for result {}".format(
                str(type(result))
            ))

        # Made it passed the if statement successfully, let's create the packet
        self.packet["result"] = self.data

    def __repr__(self):
        return "JSON-RPC Result: {}".format(repr(self.data))

    def __str__(self):
        return "<JSON-RPC {type} object - {id}>".format(
            type=self.type,
            id=self.response_id)


class JSONRPCError(JSONRPCBase):
    """
    JSON-RPC Error object
    """

    def __init__(self, code, message, data=None, response_id=None):
        """
        Create a JSON-RPC Error object
        Returns nothing on success, otherwise JSONRPCException is raised

        Parameters:
            'id':       REQUIRED, otherwise it will be set to None/NULL
            'code':     Required when creating a JSON-RPC Error object
                            MUST be type int, indicates error type
            'message':  Required when creating a JSON-RPC Error object
                            MUST be type str, short description of the error
            'data':     Required when creating a JSON-RPC Error object
                            type str or dict, contains additional information
                            about the error
        """
        self.response_id = response_id
        self.packet["id"] = self.response_id
        self.type = "Error"

        if type(code) is not int or code is None:
            raise JSONRPCException("code parameter for error MUST be type  \
                                   int!")

        if type(message) is not None and type(message) is not str:
            raise JSONRPCException("message parameter for error MUST be type \
                                   str!")

        self.code = code
        self.message = message

        self.packet["error"] = {
            "code": self.code,
            "message": self.message
            }

        if type(data) is dict:
            self.data = data
            self.packet["error"]["data"] = self.data

        elif type(data) is str:
            try:
                self.data = json.loads(data)
            except json.decoder.JSONDecodeError as e:
                # We're going to assume that it's just returning a string, not
                #   a JSON object
                self.data = data

            self.packet["error"]["data"] = self.data

        elif data is None:
            self.data = ""

        else:
            raise JSONRPCException("Unexpected data type for error {}".format(
                str(type(data))
            ))

    def __repr__(self):
        return "JSON-RPC Error: {}".format(repr(self.data))

    def __str__(self):
        return "<JSON-RPC {type} object - {id}>".format(
            type=self.type,
            id=self.response_id)
