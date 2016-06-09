"""
Test cases for the JSON-RPC module

Perfect 10.00/10 pylint score!
"""

import json_rpc
from json_rpc import JSONRPCTypes


def run_test(packet, j_type, should_pass=True):
    """
    Takes the data for the test case and displays output
    """
    success, data = json_rpc.verify_packet(packet, j_type)
    print("Pass:\t", success)
    print("Errors:  {}".format(data))
    print("Success: {}\n".format(success == should_pass))
    print("---------------------------------------------------------")

VERIFY = []

# ---------------------------------------------------
# Response tests
# ---------------------------------------------------

# Create the packet in dict form
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "result": "Success! It's working!"
}

# Append tuple:
#   packet: The JSON-RPC packet to test
#       REQUIRED
#   j_type: JSONRPCTypes object to test packet against
#       REQUIRED
#   should_pass: Boolean on whether or not it *should* pass)
#       REQUIRED - set to None if unknown what result should be
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, True))

# Fail (incorrect jsonrpc value)
TEST = {
    "jsonrpc": "3.0",
    "id": 13,
    "result": "Success! It's working!"
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (incorrect jsonrpc value, missing key "id")
TEST = {
    "jsonrpc": "3.0",
    "result": "Success! It's working!"
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, False))


# Fail (missing key "jsonrpc", missing key "result")
TEST = {
    "id": 13,
    "resul": "Success! It's working!"
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, False))


# Fail (missing key "id")
TEST = {
    "jsonrpc": "2.0",
    # "id": 13,
    "result": "Success! It's working!"
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, False))


# Fail (missing key "jsonrpc", missing key "id", missing key "result")
TEST = {
    # "jsonrpc": "2.0",
    # "id": 13,
    # "result": "Success! It's working!"
    "spam": "eggs"
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, False))

# Pass
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        "code": -32600,
        "message": "Invalid Request"
    }
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, True))

# Fail (incorrect error code)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        "code": -32601,
        "message": "Invalid Request"
    }
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (missing both "error" and "result" keys)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    # "error": {
    #     "code": -32600,
    #     "message": "Invalid Request"
    # }
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (missing error message)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        "code": -32600,
        # "message": "Invalid Request"
    }
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (missing error code)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        # "code": -32600,
        "message": "Invalid Request"
    }
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (both "error" and "result" are included)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        "code": -32600,
        "message": "Invalid Request"
    },
    "result": "Success!"
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (error code isn't type int)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        "code": "-32600",
        "message": "Invalid Request"
    }
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, False))

# Fail (error code is in range of reserved JSON-RPC codes)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "error": {
        "code": -32012,
        "message": "Invalid Request"
    }
}
VERIFY.append((TEST, JSONRPCTypes.RESPONSE, False))

# ---------------------------------------------------
# Notification tests
# ---------------------------------------------------

# Pass
TEST = {
    "jsonrpc": "2.0",
    "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    }
}
VERIFY.append((TEST, JSONRPCTypes.NOTIF, True))

# Fail (notification cannot include an 'id' key)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    }
}
VERIFY.append((TEST, JSONRPCTypes.NOTIF, False))

# Fail (missing required 'method' key, notification cannot include an 'id' key)
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    # "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    }
}
VERIFY.append((TEST, JSONRPCTypes.NOTIF, False))

# ---------------------------------------------------
# Request tests
# ---------------------------------------------------

# Pass
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    }
}
VERIFY.append((TEST, JSONRPCTypes.REQUEST, True))

# Fail (missing ID, missing required key 'method')
TEST = {
    "jsonrpc": "2.0",
    # "id": 13,
    # "method": "notify:queen_of_england",
    "params": {
        "crown": "Has been stolen"
    }
}
VERIFY.append((TEST, JSONRPCTypes.REQUEST, False))

# Fail (method starts with JSON-RPC reserved for internal use value 'rpc.')
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "method": "rpc.queen_of_england",
    "params": {
        "crown": "Has been stolen"
    }
}
VERIFY.append((TEST, JSONRPCTypes.REQUEST, False))

# Fail ('params' key isn't structured type (list or dict))
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "method": "notify:queen_of_england",
    "params": "The crown has been stolen!"
}
VERIFY.append((TEST, JSONRPCTypes.REQUEST, False))

# Fail ('method' key isn't type str,
#       'params' key isn't structured type (list or dict))
TEST = {
    "jsonrpc": "2.0",
    "id": 13,
    "method": 14,
    "params": "The crown has been stolen!"
}
VERIFY.append((TEST, JSONRPCTypes.REQUEST, False))

# ---------------------------------------
# Begin running test cases
for TEST in VERIFY:
    run_test(TEST[0], TEST[1], should_pass=TEST[2])
