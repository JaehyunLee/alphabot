from opcua_module.opcua_client import UaClient

ua_client = list()
ua_client.append(UaClient('opc.tcp://0.0.0.0:4840/optimum/device/0/'))
# ua_client.append(UaClient('opc.tcp://0.0.0.0:4841/optimum/device/1/'))
num_client = len(ua_client)


def op_guide_message():
    print('Use following example:')
    print('drive id(int) direction(f, b, l, r)')
    print('goto id(int) x(int) y(int)')


while True:
    msg = input()
    parse = msg.split()
    try:
        if parse[0] == 'drive':
            if parse[2] == 'f':
                ua_client[int(parse[1])].go_front()
            elif parse[2] == 'b':
                ua_client[int(parse[1])].go_back()
            elif parse[2] == 'l':
                ua_client[int(parse[1])].turn_left()
            elif parse[2] == 'r':
                ua_client[int(parse[1])].turn_right()
        elif parse[0] == 'goto':
            ua_client[int(parse[1])].go_to(int(parse[2]), int(parse[3]))
        elif parse[0] == 'exit':
            print('exit client')
            break
        else:
            print('Unknown Operation')
            op_guide_message()
    except IndexError:
        print('Invalid Parameter')
        op_guide_message()


for i in range(num_client):
    ua_client[i].disconnect()
