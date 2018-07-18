import datetime
from opcua import Client
from device_object import Device


class SubHandler(object):
    def __init__(self, client_object):
        self.client_object = client_object

    def datachange_notification(self, node, val, data):
        changed_timestamp = data.monitored_item.Value.SourceTimestamp
        changed_timestamp += datetime.timedelta(hours=9)
        changed_timestamp += datetime.timedelta(minutes=9)

        if node == self.client_object.location_x:
            print('[{0}] [{1}] [location_x]: {2}'.format(changed_timestamp, self.client_object.device_id, val))
        elif node == self.client_object.location_y:
            print('[{0}] [{1}] [location_y]: {2}'.format(changed_timestamp, self.client_object.device_id, val))
        elif node == self.client_object.direction:
            print('[{0}] [{1}] [direction]: {2}'.format(changed_timestamp, self.client_object.device_id, val))
        else:
            print('[{0}]: ERROR: unknown data is changed'.format(changed_timestamp))


class UaClient(object):
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.client = Client(self.server_ip)
        print('Try to connect', self.server_ip)
        self.client.connect()
        print('Connected!')

        self.root = self.client.get_root_node()
        self.device = self.root.get_child(['0:Objects', '2:device'])
        self.device_id = self.device.get_child(['2:device_id']).get_value()
        self.location_x = self.device.get_child(['2:location_x'])
        self.location_y = self.device.get_child(['2:location_y'])
        self.direction = self.device.get_child(['2:direction'])

        handler = SubHandler(self)
        sub = self.client.create_subscription(500, handler)
        sub.subscribe_data_change(self.location_x)
        sub.subscribe_data_change(self.location_y)
        sub.subscribe_data_change(self.direction)

    def go_front(self):
        self.device.call_method('2:go_front')

    def go_back(self):
        self.device.call_method('2:go_back')

    def turn_left(self):
        self.device.call_method('2:turn_left')

    def turn_right(self):
        self.device.call_method('2:turn_right')

    def go_to(self, target_x, target_y):
        self.device.call_method('2:go_to', target_x, target_y)

    def get_status(self):
        return Device(self.device).get_status()

    def disconnect(self):
        self.client.disconnect()
