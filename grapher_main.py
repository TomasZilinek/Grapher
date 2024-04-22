"""
Gaphic calculator

Created by Tomas Zilinek
no copyright but don't copy it anyway! :D

"""

from tkinter import *
import grapher_axes
import grapher_view
import grapher_assignment
import ctypes

x = 0
y = 0
assignment_n = 0
assignments = []
label_lines = []
is_timing = 0
text_focus = 0


class Mediator:
    def __init__(self):
        pass

    def draw_axes(self):
        poss = V.get_view_pos()
        A.draw(canvas, poss[0], poss[1], poss[2], poss[3], canv_width, canv_height)

    def get_input(self, n):
        return assignments[n].text.get("1.0", "end-1c")

    def text_focused(self, n):
        global text_focus
        text_focus = n

    def render(self):
        render()

    def get_line_params(self):
        global canv_height
        poss = V.get_view_pos()
        poss.append(canv_width)
        poss.append(canv_height)
        return poss

    def get_assignment_n(self):
        global assignment_n
        return assignment_n

    def get_assignment(self):
        new_assignment()

    def del_assignment(self, n):
        global text_focus, assignment_n, assignments
        del assignments[n]
        if text_focus == n:
            text_focus = 0
            if assignments[0].hidden != 1:
                assignments[0].text.focus_set()
        assignment_n -= 1
        for a in assignments:
            if a.n > n:
                a.n -= 1
        for b in assignments:
            for w in b.widgets:
                w.place_forget()
            b.show()
            if b.n == assignment_n - 2:
                b.add_button.place_forget()

    def ins_to_label(self, text, color):
        insert_to_label(text, color)

M = Mediator


def label_del_line():
    global label_lines
    global is_timing
    is_timing = 0
    for n in range(0, len(label_lines) - 1):
        label_lines[n] = label_lines[n + 1]
    if len(label_lines) != 0:
        label_lines[len(label_lines) - 1] = " "
    output_label.config(text=" ")
    for t in label_lines:
        output_label.config(text=output_label.cget("text") + str(t) + "\n")
    if len(label_lines) != 0:
        del label_lines[len(label_lines) - 1]


def insert_to_label(text, color):
    global label_lines
    global is_timing
    output_label.config(text=" ", fg=color)
    if len(label_lines) < 4:
        label_lines.append(text)
        for t in label_lines:
            output_label.config(text=output_label.cget("text") + str(t) + "\n")
    else:
        for n in range(0, 3):
            label_lines[n] = label_lines[n + 1]
        label_lines[3] = text
        output_label.config(text=" ")
        for t in label_lines:
            output_label.config(text=output_label.cget("text") + str(t) + "\n")
    root.after(6000, label_del_line)
    is_timing = 1


def new_assignment():
    global assignment_n
    assig = grapher_assignment.Assignment(assignment_frame, assignment_n, M, Tk, tk_width, tk_height, canvas)
    assignment_n += 1
    assignments.append(assig)


def released(event):
    canvas.config(cursor="fleur")
    canvas.bind("<Button-1>", clicked)


def motion(event):
    global x
    global y
    diff_x = x - event.x
    diff_y = y - event.y
    V.move(diff_x, diff_y)
    x = event.x
    y = event.y
    render()


def clicked(event):
    global x
    global y
    x = event.x
    y = event.y
    canvas.config(cursor="circle")
    canvas.bind("<ButtonRelease-1>", released)
    canvas.bind("<B1-Motion>", motion)
    # print(V.view_x1, V.view_x2)


def wheel(event):
    V.zoom(event.delta, event.x, event.y)
    render()


def render():
    canvas.delete("all")
    poss = V.get_view_pos()
    A.draw(canvas, poss[0], poss[1], poss[2], poss[3], canv_width, canv_height)
    for a in assignments:
        a.draw_line()


def clicked_tool_b(tool, tool_len):
    if assignments[0].hidden != 1:
        assignments[text_focus].text.insert(INSERT, tool)
        text_content = assignments[text_focus].text.get("1.0", "end-1c")
        if tool_len > 1:
            assignments[text_focus].text.mark_set("insert", "1." + str(text_content.find(tool) + tool_len - 1))


def right_click(event):
    print(A.range_x, A.range_y)

user32 = ctypes.windll.user32
tk_width = user32.GetSystemMetrics(0)
tk_height = user32.GetSystemMetrics(1)
geometry_str = str(tk_width) + "x" + str(tk_height)

#### root ####

root = Tk()
root.geometry(geometry_str)
root.title("grapher")
root.wm_state('zoomed')
root.bind("<Button-3>", right_click)

#### canvas_frame ####

canv_frame = Frame(root, width=tk_width * 0.78, height=tk_height * 0.95)
canv_frame.place(x=int(tk_width * 0.21), y=int(tk_height * 0.015))

canv_width = int(tk_width * 0.78)
canv_height = int(tk_height * 0.8)

canvas = Canvas(canv_frame, width=canv_width, height=canv_height)
canvas.config(background="white", cursor="fleur")
canvas.bind("<Button-1>", clicked)
canvas.bind("<MouseWheel>", wheel)
canvas.place(x=0, y=0)

output_label_height = int(tk_height - canv_height)
output_label = grapher_assignment.Widget2(canv_frame, Label, width=canv_width, height=output_label_height,
                                          text="", bg="black", fg="white", font=("arial", 15), anchor="nw",
                                          justify=LEFT)
output_label.place(x=0, y=canv_height)

#### assignment_frame ####

assignment_frame = Frame(root, width=int(tk_width * 0.2), height=int(tk_height * 0.7))
assignment_frame.config(relief=GROOVE)
assignment_frame.place(x=0, y=0)

#### tool_frame  ####

tool_frame_w = int(tk_width * 0.2)
tool_frame_h = int(tk_height * 0.3)

tool_frame = Frame(root, width=tool_frame_w, height=tool_frame_h)
tool_frame.place(x=0, y=int(tk_height * 0.7))

operants = ["x", "^", "√()", "(", ")", "π", "e", "abs()", "sin()", "cos()", "tan()", "log()"]
tool_buttons = []
tool_but_w = tool_frame_w / 7.5
border = tool_but_w / 2.5
tool_rows = 0
tool_lines = 0
tool_b_font_s = 20

for op in operants:
    if len(op) > 2:
        tool_b_font_s = int(20 - len(op) * 1.3)
    else:
        tool_b_font_s = 20
    tool_but = grapher_assignment.Widget2(tool_frame, Button, width=tool_but_w, height=tool_but_w, text=op, fg="black",
                                          font=("arial", tool_b_font_s),
                                          command=lambda tool=op, tlen=len(op): clicked_tool_b(tool, tlen))
    tool_but.place(x=border + tool_but_w * tool_rows, y=tool_lines * tool_but_w)
    tool_rows += 1
    if tool_rows == 7:
        tool_rows = 0
        tool_lines += 1

#### objects ####

new_assignment()
assignments[0].text.focus_set()
V = grapher_view.View(canv_width, canv_height)
poss = V.get_view_pos()
A = grapher_axes.Axis(canvas, poss[0], poss[1], poss[2], poss[3], canv_width, canv_height)


root.mainloop()
