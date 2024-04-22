class View:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.range_x = 0
        self.range_y = 0
        self.view_x1 = -10
        self.view_x2 = 10
        self.get_range()
        self.view_y1 = -self.range_x / self.screen_w * self.screen_h / 2
        self.view_y2 = self.view_y1 + self.range_y
        self.zoom_n = 0.15

    def get_range(self):
        if self.view_x1 <= 0 and self.view_x2 <= 0:
            self.range_x = abs(self.view_x1) - abs(self.view_x2)
        elif self.view_x1 >= 0 and self.view_x2 >= 0:
            self.range_x = self.view_x2 - self.view_x1
        elif self.view_x1 <= 0 <= self.view_x2:
            self.range_x = -self.view_x1 + self.view_x2
        self.range_y = self.range_x / self.screen_w * self.screen_h

    def get_view_pos(self):
        lst = [self.view_x1, self.view_x2, self.view_y1, self.view_y2]
        return lst

    def move(self, diff_x, diff_y):
        self.get_range()
        self.view_x1 += diff_x * self.range_x / self.screen_w
        self.view_x2 = self.view_x1 + self.range_x
        self.view_y1 += diff_y * self.range_y / self.screen_h
        self.view_y2 = self.view_y1 + self.range_y

    def zoom(self, delta, x, y):
        if delta > 0:
            self.view_x1 += self.range_x * self.zoom_n * x / self.screen_w
            self.view_x2 -= self.range_x * self.zoom_n * (self.screen_w - x) / self.screen_w
            self.view_y1 += self.range_y * self.zoom_n * y / self.screen_h
            self.get_range()
            self.view_y2 = self.view_y1 + self.range_y
        elif delta < 0:
            self.view_x1 -= self.range_x * self.zoom_n * x / self.screen_w
            self.view_x2 += self.range_x * self.zoom_n * (self.screen_w - x) / self.screen_w
            self.view_y1 -= self.range_y * self.zoom_n * y / self.screen_h
            self.get_range()
            self.view_y2 = self.view_y1 + self.range_y
