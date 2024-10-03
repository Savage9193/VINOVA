from pynput import mouse, keyboard
mouse_moves = 0
key_presses = 0
last_position = None
def on_move(x, y, gui):
    global mouse_moves, last_position
    if last_position is None:
        last_position = (x, y)
        mouse_moves += 1
        gui.log(f"Mouse moved to {x}, {y}")
    else:
        last_x, last_y = last_position
        if abs(last_x - x) > 10 or abs(last_y - y) > 10:
            mouse_moves += 1
            last_position = (x, y)
            gui.log(f"Mouse moved to {x}, {y}")

def on_press(key, gui):
    global key_presses
    try:
        gui.log(f"Key {key.char} pressed")
    except AttributeError:
        gui.log(f"Special key {key} pressed")
    key_presses += 1

def start_activity_tracking(gui):
    mouse_listener = mouse.Listener(on_move=lambda x, y: on_move(x, y, gui))
    keyboard_listener = keyboard.Listener(on_press=lambda key: on_press(key, gui))
    mouse_listener.start()
    keyboard_listener.start()

def suspend_tracking(self):
    self.is_tracking = False  
def resume_tracking(self):
    self.is_tracking = True  
