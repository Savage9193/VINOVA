from pynput import mouse, keyboard

# Global variables to track activity
mouse_moves = 0
key_presses = 0
last_position = None

def on_move(x, y):
    global mouse_moves, last_position

    # Filter mouse movements based on a threshold (e.g., 10 pixels)
    if last_position is None:
        last_position = (x, y)
        mouse_moves += 1
    else:
        last_x, last_y = last_position
        if abs(last_x - x) > 10 or abs(last_y - y) > 10:
            mouse_moves += 1
            last_position = (x, y)

def on_press(key):
    global key_presses
    try:
        # Log key presses
        print(f"Key {key.char} pressed")
    except AttributeError:
        # Log special keys
        print(f"Special key {key} pressed")
    
    key_presses += 1

def log_summary():
    global mouse_moves, key_presses
    print(f"Mouse movements: {mouse_moves}, Key presses: {key_presses}")
    mouse_moves = 0
    key_presses = 0

def start_activity_tracking():
    # Mouse Listener
    mouse_listener = mouse.Listener(on_move=on_move)
    mouse_listener.start()

    # Keyboard Listener
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
