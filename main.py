from classes import Game
from pynput import keyboard
import pywinctl as pwc
import termios, os, sys

# Get the active window at startup (should be the terminal that runs the game)
terminal = pwc.getActiveWindow()

# Globals for the game are width and height
width = 50
height = 35

def on_press(key):
    # Only detect keypresses when the active window is equal to the game window
    if pwc.getActiveWindow() == terminal:
        global user_input
        try:
            k = key.char 
        except:
            k = key.name
        user_input = k
        return False

def main():
    # Makes the cursor invisible
    print("\033[?25l", end="")
    # Clear the screen at start
    os.system('cls||clear')
    # Initialise the game
    game = Game(width, height)
    # Main game loop
    while True:
        game.draw()
        if game.checkdead():
            print("You're dead :( press q to quit or r to restart")
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
            if user_input == "r":
                game = Game(width, height)
                print("Restarted game!", end="")
            if user_input == "q":
                # Prevent all pressed keys to go to the terminal at exit
                termios.tcflush(sys.stdin.fileno(), termios.TCIOFLUSH)
                # Move cursor backward (this will overwrite "q") and print thanks
                print("\033[DThanks for playing!")
                break
            continue

        try:
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
            if user_input in ["a", "h"]:
                game.move_player("Left")
            if user_input in ["w", "k"]:
                game.move_player("Up")
            if user_input in ["s", "j"]:
                game.move_player("Down")
            if user_input in ["d", "l"]:
                game.move_player("Right")
            if user_input == "q":
                # Prevent all pressed keys to go to the terminal at exit
                termios.tcflush(sys.stdin.fileno(), termios.TCIOFLUSH)
                # Move cursor backward (this will overwrite "q") and print thanks
                print("\033[DThanks for playing!")
                break
        except:
            continue

if __name__=="__main__":
    main()
