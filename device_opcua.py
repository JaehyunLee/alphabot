import code
from opcua_module.opcua_server import UaServer

print('input your id: ')
my_device = UaServer('opc.tcp://0.0.0.0:4840/optimum/device/', input())
my_device.start()
print('device start')
try:
    embed_vars = globals()
    embed_vars.update(locals())
    shell = code.InteractiveConsole(embed_vars)
    shell.interact()
finally:
    my_device.stop()
