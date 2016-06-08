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
VERIFY.append((TEST, JSONRPCTypes.RESULT, True))

# Fail (incorrect jsonrpc value)
TEST = {
    "jsonrpc": "3.0",
    "id": 13,
    "result": "Success! It's working!"
}
VERIFY.append((TEST, JSONRPCTypes.RESULT, False))

# Fail (incorrect jsonrpc value, missing key "id")
TEST = {
    "jsonrpc": "3.0",
    "result": "Success! It's working!"
}
VERIFY.append((TEST, JSONRPCTypes.RESULT, False))


# Fail (missing key "jsonrpc", missing key "result")
TEST = {
    "id": 13,
    "resul": "Success! It's working!"
}
VERIFY.append((TEST, JSONRPCTypes.RESULT, False))


# Fail (missing key "id")
TEST = {
    "jsonrpc": "2.0",
    # "id": 13,
    "result": "Success! It's working!"
}
VERIFY.append((TEST, JSONRPCTypes.RESULT, False))


# Fail (missing key "jsonrpc", missing key "id", missing key "result")
TEST = {
    # "jsonrpc": "2.0",
    # "id": 13,
    # "result": "Success! It's working!"
    "spam": "eggs"
}
VERIFY.append((TEST, JSONRPCTypes.RESULT, False))

# Begin running test cases
for TEST in VERIFY:
    run_test(TEST[0], TEST[1], should_pass=TEST[2])
