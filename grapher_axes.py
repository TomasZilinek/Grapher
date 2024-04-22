class Axis:
    def __init__(self, canv, view_x1, view_x2, view_y1, view_y2, screen_w, screen_h):
        self.range_x = 0
        self.range_y = 0
        self.get_range(view_x1, view_x2, screen_w, screen_h)
        self.part = 0
        self.axis_x_drawn = 0
        self.axis_y_drawn = 0
        self.x_numbers_to_draw = []
        self.y_numbers_to_draw = []
        self.draw(canv, view_x1, view_x2, view_y1, view_y2, screen_w, screen_h)
        self.number_shift = 0

    def draw(self, canv, view_x1, view_x2, view_y1, view_y2, screen_w, screen_h):
        self.get_range(view_x1, view_x2, screen_w, screen_h)
        if view_y1 < 0 < view_y2:
            part_y = abs(view_y1) / (abs(view_y1) + abs(view_y2)) * screen_h
            self.axis_x_drawn = canv.create_line(0, part_y, screen_w, part_y, fill="black")
            x_axis_y_coordinate = part_y
        elif view_y1 > 0 and view_y2 > 0:
            self.axis_x_drawn = canv.create_line(0, 3, screen_w, 3, fill="black")
            x_axis_y_coordinate = 3
        else:  # (if view_y1 < 0 and view_y2 < 0:)
            self.axis_x_drawn = canv.create_line(0, screen_h - 3, screen_w, screen_h - 3, fill="black")
            x_axis_y_coordinate = screen_h - 3
        if view_x1 < 0 < view_x2:
            part_x = abs(view_x1) / (abs(view_x1) + abs(view_x2)) * screen_w
            self.axis_y_drawn = canv.create_line(part_x, screen_h, part_x, 0, fill="black")
            y_axis_x_coordinate = part_x
        elif view_x1 < 0 and view_x2 < 0:
            self.axis_y_drawn = canv.create_line(screen_w - 3, screen_h, screen_w - 3, 0, fill="black")
            y_axis_x_coordinate = screen_w - 3
        else:  # (if view_x1 > 0 and view_x2 > 0:)
            self.axis_y_drawn = canv.create_line(3, screen_h, 3, 0, fill="black")
            y_axis_x_coordinate = 3
        self.draw_numbers(canv, view_x1, view_x2, view_y1, view_y2, screen_w, screen_h, x_axis_y_coordinate, y_axis_x_coordinate)

    def get_range(self, view_x1, view_x2, screen_w, screen_h):
        if view_x1 <= 0 and view_x2 <= 0:
            range_x = abs(view_x1) - abs(view_x2)
        elif view_x1 >= 0 and view_x2 >= 0:
            range_x = view_x2 - view_x1
        else:
            range_x = -view_x1 + view_x2
        range_y = range_x / screen_w * screen_h
        self.range_x = range_x
        self.range_y = range_y

    def draw_numbers(self, canv, view_x1, view_x2, view_y1, view_y2, screen_w, screen_h, x_axis_y_coordinate, y_axis_x_coordinate):
        self.x_numbers_to_draw = []
        self.y_numbers_to_draw = []
        number_shift = self.range_x / 12
        str_shift = int(str(number_shift)[:str(number_shift).find(".")])

        # for x:

        if str_shift == 1:
            for n1 in range(int(view_x1), int(view_x2)):
                self.x_numbers_to_draw.append(n1)
        elif str_shift > 1:
            starting_point = int(view_x1 / str_shift) * str_shift
            buffer = starting_point
            while buffer <= view_x2:
                self.x_numbers_to_draw.append(buffer)
                buffer += str_shift
        part = abs(view_x2 - view_x1) / screen_w
        for x_number in self.x_numbers_to_draw:
            if x_number < 0:
                screen_x = (abs(view_x1) - abs(x_number)) / part
            elif x_number == 0:
                screen_x = (abs(view_x1) - abs(x_number)) / part + 10
            else:
                screen_x = -(view_x1 - x_number) / part
            screen_y = x_axis_y_coordinate + 20
            if x_axis_y_coordinate == screen_h - 3:
                screen_y = screen_h - 20
            canv.create_text(screen_x, screen_y, text=x_number)

        # for y:

        if str_shift == 1:
            for n2 in range(int(view_y1), int(view_y2)):
                self.y_numbers_to_draw.append(n2)
        elif str_shift > 1:
            starting_point = int(view_y1 / str_shift) * str_shift
            buffer = starting_point
            while buffer <= view_y2:
                self.y_numbers_to_draw.append(buffer)
                buffer += str_shift
        for y_number in self.y_numbers_to_draw:
            if y_number < -screen_h / 30:
                screen_y = (abs(view_y1) - abs(y_number)) / part
            elif y_number == 0:
                screen_y = (abs(view_y1) - abs(y_number)) / part + 10
            else:
                screen_y = -(view_y1 - y_number) / part
            screen_x = y_axis_x_coordinate + 20
            if y_axis_x_coordinate == screen_w - 3:
                screen_x = screen_w - 20
            canv.create_text(screen_x, screen_y, text=-y_number)  # -y_number because canvas has reversed y axis
