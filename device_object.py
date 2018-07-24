class Device(object):
    def __init__(self, device):

        self.nodeID = device.get_child(['2:device_id']).get_value()
        self.status = device.get_child(['2:status']).get_value()
        self.maxLoad = device.get_child(['2:max_load']).get_value()
        self.currentLoad = device.get_child(['2:current_load']).get_value()
        self.speed = device.get_child(['2:speed']).get_value()
        self.direction = device.get_child(['2:direction']).get_value()
        self.distanceSetPoint = device.get_child(['2:distance_set_point']).get_value()
        self.locationX = device.get_child(['2:location_x']).get_value()
        self.locationY = device.get_child(['2:location_y']).get_value()
        self.hookHeight = device.get_child(['2:hook_height']).get_value()
        self.networkCondition = device.get_child(['2:network_condition']).get_value()

    def get_status(self):
        status = {
            'nodeID': 'CRANE{0:02d}'.format(self.nodeID+1),
            'status': self.status,
            'maxLoad': self.maxLoad,
            'currentLoad': self.currentLoad,
            'speed': self.speed,
            'direction': self.direction,
            'distanceSetPoint': self.distanceSetPoint,
            'locationX': self.locationX,
            'locationY': self.locationY,
            'hookHeight': self.hookHeight,
            'networkCondition': self.networkCondition
        }
        return status

    def set_locationX(self, value):
        self.locationX = value

    def set_locationY(self, value):
        self.locationY = value

    def set_direction(self, value):
        self.direction = value

    def set_networkCondition(self, value):
        self.networkCondition = value
