import code
import time
from opcua_module.opcua_server import UaServer

my_device = UaServer('opc.tcp://0.0.0.0:4840/optimum/device/', int(input('input your id: ')))
my_device.start()
print('device start')
try:
    embed_vars = globals()
    embed_vars.update(locals())
    shell = code.InteractiveConsole(embed_vars)
    shell.interact()
finally:
    my_device.my_network_condition.set_value(0)
    time.sleep(1)
    print('Disconnected')
    my_device.stop()
