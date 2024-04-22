import math


class Line:
    def __init__(self, canv, view_x1, view_x2, view_y1, view_y2, screen_w, screen_h, equation, color, mediator, n):
        self.width = 2
        self.mode = 1
        self.already_drawn = 0
        self.neg_counter = 0
        self.counter = 0
        self.n = n
        self.able = 1
        self.mediator = mediator
        self.x = 0
        self.y = 0
        self.color = color
        self.equation = equation
        self.draw(canv, view_x1, view_x2, view_y1, view_y2, screen_w, screen_h, equation, self.color)
        self.part = 0
        self.part_back = 0

    def draw(self, canv, view_x1, view_x2, view_y1, view_y2, screen_w, screen_h, equation, color):
        self.equation = equation
        up = 0
        down = 0

        if self.equation == "":
            canv.delete("all")
            self.mediator.draw_axes("k")
        else:
            self.part = abs(view_x2 - view_x1) / screen_w
            self.part_back = self.part * 2

            self.x = view_x1

            screen_x = 0
            screen_y = 0

            prev_sc_x = screen_w
            prev_sc_y = 0

            prev_x = 0
            prev_y = 0

            while self.x < view_x2:
                try:
                    if self.neg_counter == 1:
                        self.mode = 1
                    if self.mode == 1:
                        self.x += self.part
                    else:
                        self.x += self.part / 10
                    exec("self.y = " + str(self.equation))
                    self.y = -self.y  # canvas has 0 of y-axis on the top of screen :(

                    if self.x <= 0:
                        screen_x = (abs(view_x1) - abs(self.x)) / self.part
                    else:
                        screen_x = -(view_x1 - self.x) / self.part
                    if self.y <= 0:
                        screen_y = (abs(view_y1) - abs(self.y)) / self.part
                    else:
                        screen_y = -(view_y1 - self.y) / self.part

                    if self.counter == 0:
                        if view_y1 < self.y < view_y2:
                            canv.create_line(screen_x, screen_y, screen_x, screen_y, fill=color, width=self.width)
                    elif self.counter == -1:
                        if view_y1 < self.y < view_y2:
                            canv.create_line(prev_sc_x, prev_sc_y, screen_x, screen_y, fill=color, width=self.width)
                    else:
                        if view_y1 < self.y < view_y2:
                            canv.create_line(prev_sc_x, prev_sc_y, screen_x, screen_y, fill=color, width=self.width)
                        if 0 < prev_sc_y < screen_h < screen_y:
                            canv.create_line(prev_sc_x, prev_sc_y, prev_sc_x, screen_h, fill=color, width=self.width)
                            up = 1
                        if screen_y < 0 < prev_sc_y < screen_h:
                            canv.create_line(prev_sc_x, 0, prev_sc_x, prev_sc_y, fill=color, width=self.width)
                            down = 1
                        if prev_sc_y < 0 and self.check_next(view_y1) > screen_y > screen_h:
                            canv.create_line(prev_sc_x, 0, screen_x, screen_y, fill=color, width=self.width)
                        if prev_sc_y > screen_h and self.check_next(view_y1) < screen_y < 0:
                            canv.create_line(prev_sc_x, screen_h, screen_x, 0, fill=color, width=self.width)

                    prev_sc_x = screen_x
                    prev_sc_y = screen_y
                    if up == 1:
                        prev_sc_y = screen_h + 5
                    if down == 1:
                        prev_sc_y = -5
                    self.able = 1
                    self.counter += 1
                    #if self.counter > -1:
                        #print("counter = " + str(self.counter) + ", self.x = " + str(self.x))
                    self.already_drawn = 1
                    up = 0
                    down = 0
                    if self.mode == 0:
                        print(self.mode)
                except:
                    if self.already_drawn != 0:
                        if self.counter != -1 and self.mode == 1:
                            self.x -= self.part
                            self.mode = 0
                        if self.counter != -1 and self.mode == 0:
                            self.counter = 0
                            self.neg_counter = 1
                            self.x += self.part * 2
        self.already_drawn = 0
        self.counter = 0

    def check_next(self, view_y1):
        func_y = 0
        eq = self.equation.replace("self.x", "(self.x + self.part / 1000000000000000)")
        exec("func_y = " + str(eq))
        func_y = -func_y

        if func_y <= 0:
            screen_y = (abs(view_y1) - abs(func_y)) / self.part
        else:
            screen_y = (abs(view_y1 - func_y)) / self.part

        return screen_y
