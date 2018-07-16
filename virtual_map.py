class VirtualMap(object):
    def __init__(self, location_x=0, location_y=0, direction=0):
        self.x = location_x
        self.y = location_y
        self.direction = direction

    def go_front(self):
        if self.direction == 0:
            self.y += 1
        elif self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y -= 1
        elif self.direction == 3:
            self.x -= 1
        return self.x, self.y

    def go_back(self):
        if self.direction == 0:
            self.y -= 1
        elif self.direction == 1:
            self.x -= 1
        elif self.direction == 2:
            self.y += 1
        elif self.direction == 3:
            self.x += 1
        return self.x, self.y

    def turn_left(self):
        self.direction += 1
        if self.direction > 3:
            self.direction = 0

    def turn_right(self):
        self.direction -= 1
        if self.direction < 0:
            self.direction = 3

    def go_to(self, target_x, target_y):
        op_queue = []
        tmp_x = self.x
        tmp_y = self.y
        tmp_direction = self.direction

        while tmp_x != target_x or tmp_y != target_y:
            if tmp_direction == 0:
                while tmp_y < target_y:
                    tmp_y += 1
                    op_queue.append(0)
                while tmp_y > target_y:
                    tmp_y -= 1
                    op_queue.append(1)
                if tmp_x != target_x:
                    tmp_direction = 1
                    op_queue.append(2)

            elif tmp_direction == 1:
                while tmp_x < target_x:
                    tmp_x += 1
                    op_queue.append(0)
                while tmp_x > target_x:
                    tmp_x -= 1
                    op_queue.append(1)
                if tmp_y != target_y:
                    tmp_direction = 0
                    op_queue.append(3)

            elif tmp_direction == 2:
                while tmp_y > target_y:
                    tmp_y += 1
                    op_queue.append(0)
                while tmp_y < target_y:
                    tmp_y -= 1
                    op_queue.append(1)
                if tmp_x != target_x:
                    tmp_direction = 1
                    op_queue.append(3)

            elif tmp_direction == 3:
                while tmp_x > target_x:
                    tmp_x += 1
                    op_queue.append(0)
                while tmp_x < target_x:
                    tmp_x -= 1
                    op_queue.append(1)
                if tmp_y != target_y:
                    tmp_direction = 0
                    op_queue.append(2)
        return op_queue

