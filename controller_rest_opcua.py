import datetime
from flask import Flask, request, jsonify
from opcua_module.opcua_client import UaClient


# Rest API app
app = Flask(__name__)

# OPC UA Client
ua_client = list()
ua_client.append(UaClient('opc.tcp://0.0.0.0:4840/optimum/device/0/'))
# ua_client.append(UaClient('opc.tcp://10.30.5.116:4840/optimum/device/0/'))
num_client = len(ua_client)


def drive_op(client_id, control_op):
    if control_op == 'f':
        ua_client[client_id].go_front()
    elif control_op == 'b':
        ua_client[client_id].go_back()
    elif control_op == 'l':
        ua_client[client_id].turn_left()
    elif control_op == 'r':
        ua_client[client_id].turn_right()


@app.route('/optimum/device/CRANE<int:device_id>/drive', methods=['POST'])
def drive(device_id):
    device_id -= 1
    control_op = request.args.get('op', 'NULL')

    # Error Check
    if control_op == 'NULL':
        return '[ERROR] Invalid Parameter'
    elif num_client <= device_id or device_id < 0:
        return '[ERROR] Invalid Device ID'
    else:
        drive_op(device_id, control_op)  # Move Raspberry Pi
        success_msg = '[SUCCESS][{0}][device{1}] drive {2}'
        success_msg = success_msg.format(datetime.datetime.now(), device_id, control_op)
        result_msg = {"responseCode": 2000, "responseMsg": success_msg}
        response_msg = jsonify(result_msg)
        print(response_msg)
        return response_msg


@app.route('/optimum/device/CRANE<int:device_id>/goto', methods=['POST'])
def goto(device_id):
    device_id -= 1
    location_x = request.args.get('x', 'NULL')
    location_y = request.args.get('y', 'NULL')

    # Error Check
    if location_x == 'NULL' or location_y == 'NULL':
        return '[ERROR] Invalid Parameter'
    elif num_client <= device_id or device_id < 0:
        return '[ERROR] Invalid Device ID'
    else:
        ua_client[device_id].go_to(int(location_x), int(location_y))  # Move Raspberry Pi
        success_msg = '[SUCCESS][{0}][device{1}] goto {2} {3}'
        success_msg = success_msg.format(datetime.datetime.now(), device_id, location_x, location_y)
        result_msg = {"responseCode": 2000, "responseMsg": success_msg}
        response_msg = jsonify(result_msg)
        print(response_msg)
        return response_msg


@app.route('/optimum/device/refreshStatus', methods=['POST'])
def refresh_status():
    status_msg = [ua_client[i].get_status() for i in range(num_client)]
    success_msg = '[SUCCESS][{0}]'.format(datetime.datetime.now())
    result_msg = {'responseCode': 2000, 'responseMsg': success_msg, 'opcStatus': True, 'thingsStatus': status_msg}
    result_msg = jsonify(result_msg)
    print(result_msg)
    return result_msg


app.run(host='0.0.0.0')
