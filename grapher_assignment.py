from tkinter import *
from random import randint
import grapher_line

color = ""


class Assignment:
    def __init__(self, frame, n, mediator, root, screen_w, screen_h, canv):
        self.replacements = [["^", "**"], ["√", "math.sqrt"], ["π", "math.pi"], ["e", "math.e"], ["sin", "math.sin"],
                             ["cos", "math.cos"], ["tan", "math.tan"], ["log", "math.log"]]
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.canv = canv
        self.conv = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f"}
        self.hidden = 0
        self.ass_n = 0
        self.frame_w = frame.winfo_reqwidth()
        self.n = n
        self.height = 30
        self.colors = ["red", "black", "midnight blue", "lime green", "tomato", "dark violet", "navy", "deep pink",
                       "dark green", "saddle brown", "firebrick", "blue violet", "yellow", "maroon", "orange red",
                       "blue4", "gold3", "gray30", "sienna4", "green", "gray22", "SystemHighlight", "firebrick4",
                       "chocolate", "olive drab", "dark orchid", "SpringGreen3", "purple4", "DeepSkyBlue4", "blue2"]
        self.color = self.colors[n]
        self.frame = frame
        self.text_w = int(self.frame_w * 0.7)
        self.text = Widget2(self.frame, Text, height=self.height, width=self.text_w, bg="lightgrey", font=("arial", 15))
        self.add_button = Widget2(self.frame, Button, width=30, height=30, text="+", font=("arial", 12),
                                  command=self.press_add_b, borderwidth=1)
        self.del_button = Widget2(self.frame, Button, width=30, height=30, text="X", font=("arial", 10),
                                  command=self.press_del_b)
        self.col_button = Widget2(self.frame, Button, width=30, height=30,
                                  command=self.open_col, bg=self.color)
        self.text.bind('<Return>', self.get_text)
        self.text.bind('<FocusIn>', self.got_focus)
        self.show()
        self.mediator = mediator
        self.widgets = [self.add_button, self.del_button, self.col_button, self.text]
        self.root = root
        self.col_root_opened = 0
        self.col_root = Tk
        self.got_text = ""
        self.L1 = 0
        self.line_active = 0

    def got_focus(self, event):
        self.mediator.text_focused("k", self.n)

    def get_text(self, event):
        self.got_text = self.text.get("1.0", "end-1c")
        self.text.destroy()
        del self.widgets[3]
        self.text = Widget2(self.frame, Text, height=self.height, width=self.text_w, bg="lightgrey", font=("arial", 15))
        self.text.bind('<Return>', self.get_text)
        self.text.place(x=self.frame_w * 0.05, y=self.height + self.n * self.height)
        self.text.insert(INSERT, self.got_text)
        self.text.focus_set()
        self.widgets.append(self.text)
        self.edit_str()

    def show(self):
        self.text.place(x=self.frame_w * 0.05, y=self.height + self.n * self.height)
        self.col_button.place(x=self.frame_w * 0.05 + self.text_w, y=self.height + self.n * self.height)
        self.del_button.place(x=self.frame_w * 0.05 + self.text_w + 30, y=self.height + self.n * self.height)
        self.add_button.place(x=self.frame_w * 0.07, y=self.height + (self.n + 1.2) * self.height)

    def press_add_b(self):
        if self.hidden != 1:
            self.mediator.get_assignment("k")
            self.add_button.place_forget()
        else:
            self.add_button.place_forget()
            self.col_button.config(bg=self.color)
            self.show()
            self.hidden = 0

    def press_del_b(self):
        self.ass_n = self.mediator.get_assignment_n("k")
        if self.n != 0 or self.ass_n != 1:
            self.mediator.del_assignment("k", self.n)
            self.mediator.render("k")
        self.delete()
        self.color = self.colors[self.n]
        if self.col_root_opened == 1:
            self.on_close("k")

    def delete(self):
        if self.n != 0 or self.ass_n != 1:
            for w in self.widgets:
                w.destroy()
        else:
            if self.ass_n == 1:
                self.text.insert(INSERT, ".")
                self.text.delete("1.0", "end-1c")
                self.hidden = 1
                for w in self.widgets:
                    w.place_forget()
                self.add_button.place(x=self.frame_w * 0.07, y=(self.height + 1.2))
                if self.line_active == 1:
                    del self.L1
                self.line_active = 0
                self.mediator.render("k")

    def make_col(self):
        self.color = "#"
        for _ in range(0, 6):
            put = randint(0, 15)
            if 0 <= put < 10:
                self.color += str(randint(0, 9))
            elif 10 <= put:
                self.color += self.conv[randint(0, 5)]

    def open_col(self):
        buttons = []

        def col_button(col, n):
            for b in buttons:
                b.config(borderwidth=2)
            buttons[n].config(borderwidth=6)
            global color
            color = col

        if self.col_root_opened != 1:
            self.col_root_opened = 1
            self.col_root = self.root()
            side_x = int(self.screen_w * 0.35)
            button_width = int(side_x / 7.5)
            border = button_width / 10
            side_y = int(button_width * 5)
            geom_str = str(int(button_width * 6 + border * 2)) + "x" + str(int(side_y + border * 2 + 50))
            self.col_root.geometry(geom_str)
            self.col_root.title("color picker")
            count = 0
            line = 0
            for a in range(0, 30):
                b = Widget2(self.col_root, Button, width=button_width, height=button_width,
                            bg=str(self.colors[a]), command=(lambda x=self.colors[a], y=a: col_button(x, y)))
                buttons.append(b)
                if self.colors[a] == self.color:
                    buttons[a].config(borderwidth=5)
                b.place(x=int(border + button_width * count), y=int(border + button_width * line))
                count += 1
                if count == 6:
                    line += 1
                    count = 0
            ok_width = int((int(button_width * 6 + border * 2)) / 5)
            ok = Widget2(self.col_root, Button, width=ok_width, height=40, text="OK", font=("arial", 15),
                         command=lambda x="col": self.on_close(x))
            ok.place(x=int(int(button_width * 6 + border * 2) / 2 - ok_width / 2), y=side_y + 20)
            self.col_root.protocol("WM_DELETE_WINDOW", lambda x="not_col": self.on_close(x))
            self.col_root.mainloop()

    def on_close(self, oc):
        if oc == "col":
            if color != "":
                self.color = color
                self.col_button.config(bg=self.color)
                self.draw_line()
        self.col_root.destroy()
        self.col_root_opened = 0

    def insert_str(self, index, string, str_to_insert):
        return string[:index] + str_to_insert + string[index:]

    def edit_str(self):
        new_text = []
        marks_b = ["+", "-", "/", "*", "(", ",", ".", "p", "s"]
        marks_a = ["+", "-", "/", "*", ")", ",", ".", "n"]
        symbols = ["x", "π", "e", "i"]

        for repl in self.replacements:
            self.got_text = self.got_text.replace(repl[0], repl[1])

        for symbol in symbols:
            for count, letter in enumerate(self.got_text):
                if letter == symbol and ((self.got_text[count - 1] == " " and self.got_text[count - 2] not in marks_b) or
                        (self.got_text[count - 1] != " " and self.got_text[count - 1] not in marks_b)):
                    if len(new_text) != 0:
                        if new_text[len(new_text) - 1] != "*":
                            new_text.append("*")
                    new_text.append(symbol)
                else:
                    new_text.append(letter)
                if count <= len(self.got_text) - 2:
                    if letter == symbol and ((self.got_text[count + 1] == " " and self.got_text[count + 2] not in marks_a) or
                            (self.got_text[count + 1] != " " and self.got_text[count + 1] not in marks_a)):
                        if len(new_text) != 0:
                            if new_text[len(new_text) - 1] != "*":
                                new_text.append("*")
            self.got_text = "".join(new_text)
            new_text = []

        self.got_text = self.got_text.replace("x", "self.x")
        self.create_line()

    def create_line(self):
        self.line_active = 0
        self.L1 = 0

        self.mediator.render("k")
        poss = self.mediator.get_line_params("k")
        self.L1 = grapher_line.Line(self.canv, poss[0], poss[1], poss[2], poss[3], poss[4], poss[5], self.got_text,
                self.color, self.mediator, self.n)
        self.line_active = 1

    def draw_line(self):
        if self.line_active == 1:
            poss = self.mediator.get_line_params("k")
            self.L1.draw(self.canv, poss[0], poss[1], poss[2], poss[3], poss[4], poss[5], self.got_text, self.color)


class Widget2(Frame):
    def __init__(self, master, type1, width=0, height=0, **kwargs):
        self.width = width
        self.height = height
        self.type = type1

        Frame.__init__(self, master, width=self.width, height=self.height)
        self.text_widget = self.type(self, **kwargs)
        self.text_widget.pack(expand=YES, fill=BOTH)

    def pack(self, *args, **kwargs):
        Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)

    def place(self, *args, **kwargs):
        Frame.place(self, *args, **kwargs)
        self.pack_propagate(False)

    def config(self, relief="default", borderwidth="default", bg="default", text="", fg=""):
        if relief != "default":
            self.text_widget.config(relief=relief)
        if borderwidth != "default":
            self.text_widget.config(borderwidth=borderwidth)
        if bg != "default":
            self.text_widget.config(bg=bg)
        if text != "":
            self.text_widget.config(text=text)
        if fg != "":
            self.text_widget.config(fg=fg)

    def delete(self, *args):
        self.text_widget.delete(args[0], args[1])

    def insert(self, index, text):
        self.text_widget.insert(index, text)

    def get(self, *args):
        return self.text_widget.get(args[0], args[1])

    def bind(self, *args):
        self.text_widget.bind(args[0], args[1])

    def focus_set(self):
        self.text_widget.focus_set()

    def cget(self, option):
        return self.text_widget.cget(option)

    def mark_set(self, *args):
        self.text_widget.mark_set(args[0], args[1])

    def index(self, *args):
        if args:
            self.text_widget.index(args[0])
