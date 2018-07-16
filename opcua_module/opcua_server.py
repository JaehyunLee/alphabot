from opcua import uamethod, Server, ua
from virtual_map import VirtualMap


class UaServer(object):
    def __init__(self, server_endpoint, device_id):
        self.isRaspberry = True
        try:
            import RPi.GPIO as GPIO
            from alphabot import AlphaBot2
            ab = AlphaBot2()
        except ModuleNotFoundError:
            self.isRaspberry = False

        self.server = Server()
        self.server.set_endpoint(server_endpoint + str(device_id))
        self.server.set_server_name('Optimum Server')
        uri = 'http://localhost'
        idx = self.server.register_namespace(uri)

        # Object
        self.device = self.server.nodes.objects.add_object(idx, 'device')
        self.device.add_property(idx, 'device_id', device_id)
        self.device.add_property(idx, 'status', 1)
        self.device.add_property(idx, 'max_load', 10)

        # Variable
        location_x = self.device.add_variable(idx, 'location_x', 0)
        location_x.set_writable()
        location_y = self.device.add_variable(idx, 'location_y', 0)
        location_y.set_writable()
        self.device.add_variable(idx, 'hook_height', 0)
        self.device.add_variable(idx, 'speed', 20)
        self.device.add_variable(idx, 'current_load', 0)
        self.device.add_variable(idx, 'distance_set_point', 0)
        self.device.add_variable(idx, 'current_load', 0)
        self.device.add_variable(idx, 'network_condition', True)

        self.device_direction = 0
        my_map = VirtualMap(0, 0, 0)

        @uamethod
        def go_front(parent):
            print('front')
            my_x, my_y = my_map.go_front()
            location_x.set_value(my_x)
            location_y.set_value(my_y)
            if self.isRaspberry:
                ab.forward(1.6)

        @uamethod
        def go_back(parent):
            print('back')
            my_x, my_y = my_map.go_back()
            location_x.set_value(my_x)
            location_y.set_value(my_y)
            if self.isRaspberry:
                ab.backward(1.6)

        @uamethod
        def turn_left(parent):
            print('left')
            my_map.turn_left()
            if self.isRaspberry:
                ab.left(0.4)

        @uamethod
        def turn_right(parent):
            print('right')
            my_map.turn_right()
            if self.isRaspberry:
                ab.right(0.4)

        @uamethod
        def go_to(parent, target_x, target_y):
            op_queue = my_map.go_to(target_x, target_y)
            print('op_queue:', op_queue)
            while len(op_queue) > 0:
                device_op = op_queue.pop(0)
                if device_op == 0:
                    go_front(parent)
                elif device_op == 1:
                    go_back(parent)
                elif device_op == 2:
                    turn_left(parent)
                elif device_op == 3:
                    turn_right(parent)

        # Method
        self.device.add_method(idx, 'go_front', go_front)
        self.device.add_method(idx, 'go_back', go_back)
        self.device.add_method(idx, 'turn_left', turn_left)
        self.device.add_method(idx, 'turn_right', turn_right)
        self.device.add_method(idx, 'go_to', go_to, [ua.VariantType.Int64, ua.VariantType.Int64])


    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop()
