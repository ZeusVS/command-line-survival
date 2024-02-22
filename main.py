import os
import time
import random


class Character():
    def __init__(self, location):
        self._health = 100
        self._location = location

    def get_location(self):
        return self._location

    def get_health(self):
        return self._health
    
    def heal(self, amount):
        self._health += amount

    def damage(self, amount):
        self._health -= amount

    def set_location(self, location):
        self._location = location


class Cell():
    def __init__(self):
        self.hidden = True
    def draw(self):
        if self.hidden:
            return "██"
        else:
            return self.symbol()
    def symbol(self):
        pass


class Empty(Cell):
    def symbol(self):
        return "  "

class Monster(Cell):
    def symbol(self):
        return "\033[31m☻ \033[0m"

class Health(Cell):
    def symbol(self):
        return "\033[32m✚ \033[0m"

class Game():
    def __init__(self, width, height):
        self._width = width
        self._height = height

        self.create_map()
        self.create_player()
        self.update_los()

    def create_player(self):
        # Create the player character at random location
        x = random.randint(0, self._width - 1)
        y = random.randint(0, self._height - 1)
        location = [x, y]
        self._player = Character(location)
        # Make sure the square under the player is an empty cell
        self._grid[x][y] = Empty()

    def create_map(self):
        # All possible tiles
        tiles = (Empty, Monster, Health)
        weights = (75, 20, 5)
        # Create the map of the game as a grid
        # Every element of the grid is a Cell object
        self._grid = []
        for x in range(self._width):
            self._grid.append([])
            for y in range(self._height):
                cell = random.choices(tiles, weights, k=1)[0]()
                self._grid[x].append(cell)
    
    def move_player(self, direction):
        location = self._player.get_location()

        if direction in ["n", "north"]:
            if location[1] == 0:
                raise Exception("Out of bounds")
            location[1] -= 1
        elif direction in ["s", "south"]:
            if location[1] == self._height - 1:
                raise Exception("Out of bounds")
            location[1] += 1
        elif direction in ["e", "east"]:
            if location[0] == self._width - 1:
                raise Exception("Out of bounds")
            location[0] += 1
        elif direction in ["w", "west"]:
            if location[0] == 0:
                raise Exception("Out of bounds")
            location[0] -= 1
        else:
            raise Exception("Unexpected input")

        self._player.set_location(location)
        self.update_los()
    
    def update_los(self):
        # Update line of sight after every time the player has moved
        # Vision is the distance of the LOS, hardcoded atm
        vision = 1
        x = self._player.get_location()[0]
        y = self._player.get_location()[1]
        for diffx in range(-vision, vision + 1):
            for diffy in range(-vision, vision + 1):
                if abs(diffx) + abs(diffy) <= vision:
                    if 0 <= x + diffx <= self._width - 1 and \
                            0 <= y + diffy <= self._height - 1:
                        self._grid[x + diffx][y + diffy].hidden = False

    def draw(self):
        # Using escape codes to give color to the different parts
        red = "\033[31m"
        blue = "\033[34m"
        reset = "\033[0m"
        # First clear the screen and then redraw the entire map
        # Had to use to escape code shenanigans because clr caused too much flickering
        # Go up one line and delete whole line to clear the input text
        print('\033[A', end="")
        print('\033[J', end="")
        # Put cursor at the home position to start overwriting everyting
        print('\033[H', end="")

        # We put everything in one big string and then print the entire screen at once
        # This prevents some weirdness happening when giving an input between prints
        toprint = ""
        # Print title of the game
        toprint += f"{red}Command Line Survival{reset}".center((self._width + 2) * 2) + "\n\n"
        # Print upper border
        toprint += f"{red}▒▒{reset}" * (self._width + 2) + "\n"
        # Print main game area
        for y in range(self._height):
            for x in range(self._width):
                # Print left border
                if x == 0:
                    toprint += f"{red}▒▒{reset}"
                # If the current cell is the location of the player, print *
                if self._player.get_location() == [x, y]:
                    toprint += f"{blue}☻ {reset}"
                else:
                    toprint += self._grid[x][y].draw()
            # Print right border
            toprint += f"{red}▒▒{reset}" + "\n"
        # Print lower border
        toprint += f"{red}▒▒{reset}" * (self._width + 2)
        # Print player stats
        toprint += "\n\n"
        toprint += "Player\n"
        toprint += f"Health: {self._player.get_health()}"
        toprint += "\n\n"
        print(toprint, end="")


def main():
    # Clear the screen at start
    os.system('cls||clear')
    # Initialise the game
    game = Game(width = 50, height = 35)
    # Main game loop
    while True:
        game.draw()
        direction = input("Move North, East, South or West?\n(q to exit game)\n").lower()
        if direction == "q":
            print("Thanks for playing!")
            break
        try:
            game.move_player(direction)
        except Exception as e:
            continue

if __name__=="__main__":
    main()
