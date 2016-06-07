"""
A simple JSON-RPC packet creation module for Python 3
Created by RPiAwesomneness for use with the CactusBot project
"""

import json


class JSONRPCException(Exception):
    """
    Custom exception used within JSONRPCResult and JSONRPCError
    """

    def __init__(self, message):
        super(JSONRPCException, self).__init__()
        self.message = message

    def __repr__(self):
        return "Creation of JSON-RPC packet failed because: {}".format(
            self.message)

    def __str__(self):
        return "Creation of JSON-RPC packet failed because: {}".format(
            self.message)


class JSONRPCResult:
    """
    JSON-RPC Result object
    """
    response_id = 0
    packet = {
        "jsonrpc": "2.0",        # Default required key/value pair for JSON-RPC
        "id": response_id
    }

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

        if isinstance(result, dict):
            self.data = result
        elif isinstance(result, str):
            self.data = json.loads(result)
        else:
            raise JSONRPCException("Unexpected data type for result {}".format(
                str(type(result))
            ))

        # Made it passed the if statement successfully, let's create the packet
        self.packet["result"] = self.data

    def return_packet(self):
        """
        Simple method to satisfy pylint
        Just returns the JSON-RPC packet
        """
        return self.packet

    def update_packet(self, **kwargs):
        """
        Allows you to update the packet's key/data pairs via a method
        """
        for arg in kwargs:
            if arg in self.packet:
                self.packet[arg] = kwargs[arg]
            elif arg in self.packet["result"]:
                self.packet["result"][arg] = kwargs[arg]

    def __repr__(self):
        return "JSON-RPC Result: {}".format(repr(self.data))

    def __str__(self):
        return "<JSON-RPC {type} object - {id}>".format(
            type=self.type,
            id=self.response_id)


class JSONRPCError:
    """
    JSON-RPC Error object
    """
    response_id = 0
    packet = {
        "jsonrpc": "2.0",        # Default required key/value pair for JSON-RPC
        "id": response_id
    }

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

        if isinstance(code, int) is not True or code is None:
            raise JSONRPCException("code parameter for error MUST be type  \
                                   int!")

        if code is None and isinstance(message, str) is not True:
            raise JSONRPCException("message parameter for error MUST be type \
                                   str!")

        self.code = code
        self.message = message

        self.packet["error"] = {
            "code": self.code,
            "message": self.message
        }

        if isinstance(data, dict):
            self.data = data
            self.packet["error"]["data"] = self.data

        elif isinstance(data, str):
            try:
                self.data = json.loads(data)
            except json.decoder.JSONDecodeError:
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

    def return_packet(self):
        """
        Simple method to satisfy pylint
        Just returns the JSON-RPC packet
        """
        return self.packet

    def update_packet(self, **kwargs):
        """
        Allows you to update the packet's key/data pairs via a method
        """
        for arg in kwargs:
            if arg in self.packet:
                self.packet[arg] = kwargs[arg]
            elif arg in self.packet["error"]:
                self.packet["result"][arg] = kwargs[arg]

    def __repr__(self):
        return "JSON-RPC Error: {}".format(repr(self.data))

    def __str__(self):
        return "<JSON-RPC {type} object - {id}>".format(
            type=self.type,
            id=self.response_id)
