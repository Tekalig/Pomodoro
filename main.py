from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
resp = 1
timer = None
toggle = True


# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    window.after_cancel(timer)
    canvas.itemconfig(time_text, text="00:00")
    start_bt.config(image=start_image)
    pomodoro_count.config(text="")
    status.config(text="Timer")
    global resp, toggle
    resp = 1
    toggle = True


# ---------------------------- TIMER MECHANISM ------------------------------- #
def time_setup():
    global resp
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    if resp % 2:
        status.config(text="Work", foreground=GREEN)
        count_down(work_sec)
    elif resp % 8 == 0:
        status.config(text="Long Break", foreground=RED)
        count_down(long_break_sec)
    else:
        status.config(text="Break", foreground=PINK)
        count_down(short_break_sec)
    resp += 1


# ---------------------------- TOGGLE  ------------------------------- #
def start_stop():
    global toggle
    mine, sec = map(int, canvas.itemcget(time_text, "text").split(":"))
    sec += mine * 60
    if toggle:
        if sec == 0:
            time_setup()
        else:
            count_down(sec)
        toggle = False
        start_bt.config(image=stop_image)
    else:
        window.after_cancel(timer)
        start_bt.config(image=start_image)
        toggle = True


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(mine):
    canvas.itemconfig(time_text, text=f"{mine // 60:02}:{mine % 60:02}")
    global timer
    if mine > 0:
        timer = window.after(1000, count_down, mine - 1)
    else:
        time_setup()
        marks = ""
        for _ in range((resp - 1) // 2):
            marks += "@"
        pomodoro_count.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=120, pady=60, background=YELLOW)

# create a Status text
status = Label(text="Timer", font=(FONT_NAME, 24, "bold"), foreground=GREEN, background=YELLOW)
status.grid(row=0, column=1)

# create a canvas
canvas = Canvas(width=200, height=224, background=YELLOW, borderwidth=0, highlightthickness=0)

# create image
tomato_image = PhotoImage(file="./tomato.png")
canvas.create_image(100, 112, image=tomato_image)

# create time text
time_text = canvas.create_text(100, 130, text="00:00", font=(FONT_NAME, 34, "bold"))
canvas.grid(row=1, column=1)

# start button
stop_image = PhotoImage(file="./icons8-stop-64.png")
start_image = PhotoImage(file="./icons8-start-button-64.png")
start_bt = Button(text="start", image=start_image, command=start_stop, highlightthickness=0, borderwidth=0)
start_bt.grid(row=2, column=0)

# count the number of pomodoro you finished
pomodoro_count = Label(text="", foreground=GREEN, background=YELLOW, font=(FONT_NAME, 24, "bold"))
pomodoro_count.grid(row=3, column=1)

# reset button
reset_image = PhotoImage(file="./icons8-reset-50.png")
reset_bt = Button(text="reset", image=reset_image, command=reset, highlightthickness=0, borderwidth=0)
reset_bt.grid(row=2, column=2)

if __name__ == "__main__":
    window.mainloop()
