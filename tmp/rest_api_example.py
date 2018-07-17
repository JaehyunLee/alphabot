import datetime
from flask import Flask, request, json, jsonify
app = Flask(__name__)


@app.route('/optimum/device/<int:device_id>/goto', methods=['POST'])
def goto(device_id):
    location_x = request.args.get('x', 'NULL')
    location_y = request.args.get('y', 'NULL')
    success_msg = '[SUCCESS][{0}][device{1}] goto {2} {3}'
    success_msg = success_msg.format(datetime.datetime.now(), device_id, location_x, location_y)
    print(success_msg)
    if location_x == 'NULL' or location_y == 'NULL':
        return '[ERROR] Invalid Parameter'
    return success_msg


@app.route('/optimum/device/<int:device_id>/refreshStatus', methods=['POST'])
def refresh_status(device_id):
    status_list = {'test': device_id, 'test2': device_id}
    status_json = jsonify(json.dumps(status_list))
    print('[SUCCESS][{0}][device{1}]'.format(datetime.datetime.now(), device_id), end=' ')
    print(status_json)
    if device_id == 'NULL':
        return '[ERROR] Invalid Parameter'
    return status_json


app.run(host='0.0.0.0')
