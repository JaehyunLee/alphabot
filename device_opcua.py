import code
from opcua_module.opcua_server import UaServer

my_device = UaServer('opc.tcp://0.0.0.0:4840/optimum/device/', 0)
my_device.start()
try:
    embed_vars = globals()
    embed_vars.update(locals())
    shell = code.InteractiveConsole(embed_vars)
    shell.interact()
finally:
    my_device.stop()
