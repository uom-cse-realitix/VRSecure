class point:
    def __init__(self, image_width, image_height):
        self.x_1 = image_width
        self.x_2 = image_width
        self.y_1 = image_height
        self.y_2 = image_height

    def set_x_coordinates(self, x_1, x_2):
        self.x_1 = int(self.x_1 * x_1)
        self.x_2 = int(self.x_2 * x_2)

    def set_y_coordinates(self, y_1, y_2):
        self.y_1 = int(self.y_1 * y_1)
        self.y_2 = int(self.y_2 * y_2)

    def get_mid_point(self):
        return (self.x_1 + self.x_2) / 2, (self.y_1 + self.y_2) / 2

    def get_x_coordinates(self):
        return self.x_1, self.x_2

    def get_y_coordinates(self):
        return self.y_1, self.y_2

    def get_top_left(self):
        return self.x_1, self.y_1

    def get_bottom_right(self):
        return self.x_2, self.y_2

    def get_top_right(self):
        return self.x_2, self.y_1
