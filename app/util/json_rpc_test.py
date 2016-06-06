import json_rpc

foo = json_rpc.JSONRPCResult(response_id=1,
                             result={"foo": "bar"}
                             )

print(repr(foo))
print(foo)
print(foo.packet)

foo = json_rpc.JSONRPCError(response_id=10,
                            code=-32600,
                            message="Invalid Request",
                            )

print()
print(repr(foo))
print(foo)
print(foo.packet)

foo = json_rpc.JSONRPCError(response_id=13,
                            code=202,
                            message="Success creating ticket",
                            data={"spam": "eggs"}
                            )

print()
print(repr(foo))
print(foo)
print(foo.packet)
