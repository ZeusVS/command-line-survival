import os


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
        self._type = "empty"
        self.hidden = True
    def __str__(self):
        if self.hidden:
            return "?"
        else:
            return " "


class Game():
    def __init__(self, width, height):
        self._width = width
        self._height = height

        self.create_map()
        self.create_player()
        self.update_los()

    def create_player(self):
        # Create the player character
        location = [0, 0]
        self._player = Character(location)

    def create_map(self):
        # Create the map of the game as a grid
        # Every element of the grid is a Cell object
        self._grid = []
        for x in range(self._width):
            self._grid.append([])
            for y in range(self._height):
                cell = Cell()
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
        vision = 3
        x = self._player.get_location()[0]
        y = self._player.get_location()[1]
        for diffx in range(-vision, vision):
            for diffy in range(-vision, vision):
                if abs(diffx) + abs(diffy) < vision:
                    self._grid[x + diffx][y + diffy].hidden = False

    def draw(self):
        # First clear the screen and then redraw the entire map
        os.system('cls||clear')
        print("Command Line Survival".center(self._width))
        print()
        for y in range(self._height):
            for x in range(self._width):
                # If the current cell is the location of the player, print *
                if self._player.get_location() == [x, y]:
                    print("*", end="")
                else:
                    print(self._grid[x][y], end="")
            print()
        # Print player stats
        print()
        print("Player")
        print(f"Health: {self._player.get_health()}")
        print()


def main():
    # Initialise the game
    game = Game(width = 80, height = 35)
    # Main game loop
    while True:
        game.draw()
        direction = input("Move North, East, South or West?\n(q to exit game)\n").lower()
        if direction == "q":
            break
        try:
            game.move_player(direction)
        except Exception as e:
            continue

if __name__=="__main__":
    main()
