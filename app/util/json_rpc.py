"""
A simple JSON-RPC 2.0 module for Python 3
Created by RPiAwesomneness for use with the CactusBot project

Perfect 10.00/10 pylint score!
"""

import json
from json import JSONDecodeError
import enum


class JSONRPCTypes(enum.IntEnum):
    """
    Enum-type class to provide easy identification of packet typ
    """
    RESULT = 0
    ERROR = 1
    NOTIF = 2


def _verify_error_contents(packet):
    """
    Verify the contents of a result packet
        - Returns False, list of errors if verification fails
                            OR
        - Returns True, None if passes verification
    """
    for key in ("error", "id"):
        if key not in packet:
            return False, JSONRPCException("Packet missing required "
                                           "key {}".format(key))

    # At this point, all required keys are present
    if not isinstance(packet["code"], int):
        return False, JSONRPCException("Error key 'code' type is required to"
                                       " be type int, got type {}".format(
                                           type(packet["code"])))

    # Check if packet["code"] is a JSON-RPC reserved code & if so,
    #   does packet["message"] match?

    # Success, execution to this point means the packet has passed
    return True, packet


def _verify_result_contents(packet):
    """
    Verify the contents of a result packet
        - Returns False, list of errors if verification fails
                            OR
        - Returns True, None if passes verification
    """
    err_return = []
    failed = False

    for key in ("result", "id"):
        if key not in packet:
            err_return.append("Missing required key '{}'".format(key))
            failed = True

    if failed:
        return False, err_return
    else:
        # Success, execution to this point means the packet has passed
        return True, None


def _verify_notif_contents(packet):
    """
    Verify the contents of a result packet
        - Returns False, list of errors if verification fails
                            OR
        - Returns True, None if passes verification
    """
    for key in ("tuple", "of", "required", "keys"):
        if key not in packet:
            return False, JSONRPCException("Packet missing required "
                                           "key {}".format(key))

    # Success, execution to this point means the packet has passed
    return True, packet


def _check_json(packet):
    """
    Checks if data is a string or a dictionary and then returns:
        - True and the JSON in dict form if it's valid JSON (True, dict)
                                OR
        - False and a traceback object if it's invalid JSON (False, traceback)
    """
    if isinstance(packet, str):
        # Attempt to decode the string into a dictionary
        try:
            data = json.loads(packet)
        except JSONDecodeError as exception:
            # It's not valid JSON
            return False, exception

        # Made it past the try/except, that means it's valid JSON
        return True, data

    elif isinstance(packet, dict):
        # Already in dictionary form
        data = packet
        return True, data

    elif isinstance(packet, bytes):
        # In bytes form, let's convert to utf-8 str
        decoded = packet.decode('utf-8')

        # SO MUCH META O_O
        # Dude, it's just a recursive call
        # SHUT UP. BEING SUPER META IS WAY COOLER

        # Recursively called with decoded string, will return success/fail
        return _check_json(decoded)

    else:
        # It's something else, so fail since we can't check it
        return False, JSONRPCException("Unable to validate data of "
                                       "type {}".format(type(packet)))


def verify_packet(packet, j_type):
    """
    Verifies whether or not 'packet' is a JSON-RPC compliant packet
    Arguments:
        'packet':   REQUIRED - JSON-encoded str or dict to be verified
        'j_type':   REQUIRED - "error" or "response", tells function what
                        type of JSON-RPC packet to verify 'packet' against
    Example:
        foo = {
            "jsonrpc": "2.0",
            "id": 13,
            "result": "Success! It's working!"
        }
        json_rpc.verify_packet(foo, JSONRPCTypes.RESULT)    # Will return True
    """
    # Check initially, if it's not a string, there's not point in continuing
    #   any further, save time/CPU cycles
    if j_type not in (JSONRPCTypes.ERROR,
                      JSONRPCTypes.NOTIF,
                      JSONRPCTypes.RESULT):
        return False, JSONRPCException("Incorrect type {}. Expected "
                                       "JSONRPCTypes object".format(j_type))

    success, data = _check_json(packet)

    if not success:
        # It's either not a string or not a dict, so we can't work with it
        return False, data

    # Errors to return to the user
    errors = []
    # Innocent until proven guilty!
    failed = False

    # Check for 'jsonrpc': '2.0' required key/value pair
    if "jsonrpc" not in data:
        # Required key 'jsonrpc' doesn't exist, so fail
        errors.append("Missing required key 'jsonrpc'")
        # Failed the validation
        failed = True
    elif data["jsonrpc"] != "2.0":
        # 'jsonrpc' key DOES exist, but doesn't have correct value
        errors.append("'jsonrpc' key has incorrect value {}".format(
            data["jsonrpc"])
                     )
        # Failed the validation
        failed = True

    if j_type == JSONRPCTypes.ERROR:
        print("Type:\t ERROR")
        # Begin checking if it's a correct error packet
        success, data = _verify_error_contents(data)
    elif j_type == JSONRPCTypes.RESULT:
        print("Type:\t RESULT")
        # Begin checking if it's a correct result packet
        success, data = _verify_result_contents(data)
    elif j_type == JSONRPCTypes.NOTIF:
        print("Type:\t NOTIF")
        # Begin checking if it's a correct notification packet
        success, data = _verify_notif_contents(data)
    else:
        # It's not "error" or "result", so return error
        return False, "type {} is unknown: it must be either error, result, " \
            "or notification"

    if not success:
        failed = True
        errors.extend(data)

    if failed:
        # Packet failed validation somewhere, return False and a list of
        #   failures
        return False, errors
    else:
        # Success! Packet is JSON-RPC compliant
        return True, None


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

        Arguments:
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
            try:
                self.data = json.loads(result)
            except JSONDecodeError:
                # It's not actual JSON, so just return the actual data
                self.data = result
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

        Arguments:
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


# Add reserved JSON-RPC codes/pre-created error responses
