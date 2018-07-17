from opcua_module.opcua_client import UaClient

ua_client = list()
ua_client.append(UaClient('opc.tcp://172.17.1.92:4840/optimum/device/0/'))
ua_client.append(UaClient('opc.tcp://172.17.3.141:4840/optimum/device/1/'))
num_client = len(ua_client)


def op_guide_message():
    print('Use following example:')
    print('goto id(int) x(int) y(int)')
    print('drive id(int) direction(f, b, l, r)')
    print('lets direction(f, b, l, r)')


def drive(client_id, control_op):
    if control_op == 'f':
        ua_client[client_id].go_front()
    elif control_op == 'b':
        ua_client[client_id].go_back()
    elif control_op == 'l':
        ua_client[client_id].turn_left()
    elif control_op == 'r':
        ua_client[client_id].turn_right()


while True:
    msg = input()
    parse = msg.split()
    try:
        if parse[0] == 'drive':
            drive(int(parse[1]), parse[2])
        elif parse[0] == 'goto':
            ua_client[int(parse[1])].go_to(int(parse[2]), int(parse[3]))
        elif parse[0] == 'lets':
            for i in range(num_client):
                drive(i, parse[1])
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
