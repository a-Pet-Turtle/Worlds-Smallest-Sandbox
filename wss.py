import tkinter as tk
import time
import random

# -------------------------
# Globals
# -------------------------
parxsand = []
parysand = []
paridsand = []

parxwater = []
parywater = []
paridwater = []

frame_count = 0
frame_skip = 2
target_fps = 100
speed = 10  # ms between frames

# -------------------------
# Setup window & canvas
# -------------------------
win = tk.Tk()
win.title("World's Smallest Sandbox")
win.config(bg="Black")
win.resizable(False, False)

head = tk.Label(win, text="World's Smallest Sandbox", font=("Comic Sans MS", 10, "bold italic"), fg="yellow", bg="black")
game = tk.Canvas(win, width=190, height=80, bg="Black", bd=0, highlightthickness=0)
head.pack(pady=1)
game.pack()


# Stats window
statwin = tk.Toplevel(win)
statwin.title("WSS Statistics")
elapsedtime = tk.Label(statwin, text="FPS: N/A")
waterpars = tk.Label(statwin, text="Water: 0 particles")
sandpars = tk.Label(statwin, text="Sand: 0 particles")
waterpars.pack()
sandpars.pack()
elapsedtime.pack()


# -------------------------
# Utility
# -------------------------
def in_bounds(x, y):
    return 0 <= x < 190 and 0 <= y < 80

def water_at(x, y):
    for i in range(len(parxwater)):
        if parxwater[i] == x and parywater[i] == y:
            return i
    return None

def occupied(x, y):
    if not in_bounds(x, y):
        return True
    for i in range(len(parxsand)):
        if parxsand[i] == x and parysand[i] == y:
            return True
    for i in range(len(parxwater)):
        if parxwater[i] == x and parywater[i] == y:
            return True
    return False

# -------------------------
# Particle update
# -------------------------
def updatesand(i):
    x = parxsand[i]
    y = parysand[i]
    pid = paridsand[i]

    # Down
    w_idx = water_at(x, y+1)
    if not occupied(x, y+1):
        parysand[i] += 1
        game.move(pid, 0, 1)
        return
    elif w_idx is not None:
        # Try to move water to valid position
        for dx in [0, -1, 1]:
            new_x = parxwater[w_idx] + dx
            new_y = parywater[w_idx] - 1
            if in_bounds(new_x, new_y) and not occupied(new_x, new_y) and water_at(new_x, new_y) is None:
                game.move(paridwater[w_idx], new_x - parxwater[w_idx], new_y - parywater[w_idx])
                parxwater[w_idx] = new_x
                parywater[w_idx] = new_y
                parysand[i] += 1
                game.move(pid, 0, 1)
                return

    # Diagonal left
    if not occupied(x-1, y+1):
        parxsand[i] -= 1
        parysand[i] += 1
        game.move(pid, -1, 1)
        return
    w_idx = water_at(x-1, y+1)
    if w_idx is not None:
        for dx in [0, -1, 1]:
            new_x = parxwater[w_idx] + dx
            new_y = parywater[w_idx] - 1
            if in_bounds(new_x, new_y) and not occupied(new_x, new_y) and water_at(new_x, new_y) is None:
                game.move(paridwater[w_idx], new_x - parxwater[w_idx], new_y - parywater[w_idx])
                parxwater[w_idx] = new_x
                parywater[w_idx] = new_y
                parxsand[i] -= 1
                parysand[i] += 1
                game.move(pid, -1, 1)
                return

    # Diagonal right
    if not occupied(x+1, y+1):
        parxsand[i] += 1
        parysand[i] += 1
        game.move(pid, 1, 1)
        return
    w_idx = water_at(x+1, y+1)
    if w_idx is not None:
        for dx in [0, -1, 1]:
            new_x = parxwater[w_idx] + dx
            new_y = parywater[w_idx] - 1
            if in_bounds(new_x, new_y) and not occupied(new_x, new_y) and water_at(new_x, new_y) is None:
                game.move(paridwater[w_idx], new_x - parxwater[w_idx], new_y - parywater[w_idx])
                parxwater[w_idx] = new_x
                parywater[w_idx] = new_y
                parxsand[i] += 1
                parysand[i] += 1
                game.move(pid, 1, 1)
                return

def updatewater(i):
    x = parxwater[i]
    y = parywater[i]
    pid = paridwater[i]

    # Down
    if not occupied(x, y+1):
        parywater[i] += 1
        game.move(pid, 0, 1)
        return

    dirs = [-1, 1]
    random.shuffle(dirs)

    # Diagonal first
    for d in dirs:
        if not occupied(x + d, y + 1):
            parxwater[i] += d
            parywater[i] += 1
            game.move(pid, d, 1)
            return

    # Sideways
    for d in dirs:
        if not occupied(x + d, y):
            parxwater[i] += d
            game.move(pid, d, 0)
            return

# -------------------------
# Particle creation
# -------------------------
def addsand(x, y):
    parxsand.append(x)
    parysand.append(y)
    paridsand.append(game.create_rectangle(x, y, x, y, outline="", fill="yellow"))

def addwater(x, y):
    parxwater.append(x)
    parywater.append(y)
    paridwater.append(game.create_rectangle(x, y, x, y, outline="", fill="blue"))

# -------------------------
# Mouse
# -------------------------
def mouseleft(event):
    addsand(event.x, event.y)

def mouseright(event):
    addwater(event.x, event.y)

# -------------------------
# Frame skipping loop
# -------------------------
frame_count = 0
frame_skip = 2

def gameloop():
    global frame_count, frame_skip

    start = time.time()
    frame_count += 1
    steps = 1 if frame_skip == 1 else 2

    if frame_count % frame_skip == 0:
        for _ in range(steps):
            for i in reversed(range(len(parxsand))):
                updatesand(i)
            for i in reversed(range(len(parxwater))):
                updatewater(i)

    frame_time = time.time() - start
    fps = 1 / frame_time if frame_time > 0 else 0
    elapsedtime.config(text=f"FPS: {fps:.1f} | Skip: {frame_skip}")
    waterpars.config(text=f"Water: {len(parxwater)}")
    sandpars.config(text=f"Sand: {len(parxsand)}")

    # Adaptive frame skipping
    if fps < target_fps * 0.7:
        frame_skip = min(frame_skip + 1, 5)
    elif fps > target_fps * 1.2:
        frame_skip = max(frame_skip - 1, 1)

    win.after(speed, gameloop)

# -------------------------
# Bind & start
# -------------------------
win.bind("<B1-Motion>", mouseleft)
win.bind("<Button-1>", mouseleft)
win.bind("<B3-Motion>", mouseright)
win.bind("<Button-3>", mouseright)

game.create_text(95, 40, text="(Drag to create sand)", font=("Comic Sans MS", 9), fill="Yellow")
win.after(0, gameloop)
win.mainloop()