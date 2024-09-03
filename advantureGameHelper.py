from __future__ import annotations

from typing import Optional, TextIO
import pickle
import os


ORIGIN = 1
DEFAULT_FILE_NAME = "anonymous"

SPECIAL_ITEMS = ["T-card", "Lucky Pen", "Cheat Sheet"]
FOOD = ["Broccoli with garlic", "Greek salad", "Chicken breast"]
DIRECTIONS = ["north", "south", "east", "west"]
LOCATION_WARNING = """Warning. You have reached the edge of the map.
You may want to undo your last move to avoid wasting time in this nowhere."""


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - number
        The number of the location
        - name
        The name of the location
        - points
        How many points will be awarded for the first visit
        - brief_description
        A short desciption displayed when second visit is made.
        - long_description.
        A complete description displayed when player choose to look
        or visited first time.
        - position: Optional[tuple[int, int]]
        The position relative to world map. May be left as None.
        - _visits
        The number of times where the player has been to the location.
    """

    number: int
    name: str
    points: int
    brief_description: str
    long_description: str
    position: Optional[tuple[int, int]]
    _visits: int

    def __init__(self, number: int, name: str, points: int, descriptions: tuple[str]) -> None:
        """Initialize a new location.
        """

        self.number = number
        self.name = name
        self.points = points
        self.brief_description = descriptions[0]
        self.long_description = descriptions[1]
        self.position = None
        self._visits = 0

    def __str__(self) -> str:
        return f"Location({self.number}, {self.name}, {self.points}, {self.brief_description})"

    def __repr__(self) -> str:
        return self.__str__()

    def register_visit(self) -> None:
        """
        Abstract method for sub-class to inherit for modification.
        """
        self._visits += 1

    def get_state(self) -> Location:
        """
        Abstract method for sub-class to inherit for modification.
        """
        return self

    def get_points(self) -> int:
        """
        Returns the points of the corresponding location
        """
        return self.get_state().points

    def get_brief(self) -> str:
        """
        Returns the breif description of the corresponding location
        """
        return self.get_state().brief_description

    def get_long(self) -> str:
        """
        Returns the long description of the corresponding location
        """
        return self.get_state().long_description


class SequentialLocation(Location):
    """
    A special location class used to represent the 100s.

    An instance of the SequantialLocation class contains a base state and a sequence
    of possible states (in terms of Location class).
    The attrbitues align with the parent class describe the base case.

    Instance Attributes:
        - _next_states:
        Contains a list of all possible Locations that may take over the base location
        depending on time conditions.
        - _state_pointer:
        Points to the current time-state corresponding to the physical location.
        If _state_pointer = n. Then n=-1 or n >= len(_next_states) represents the base case.
        Otherwise, it point to the n^th element in the list _next_states


    Representation Invariants:
        - self._syaye_pointer >= -1
    """
    _next_states: list[Location]
    _state_pointer: int

    def __init__(self, number: int, name: str, points: int, descriptions: tuple[str, str]) -> None:
        super().__init__(number, name, points, descriptions)
        self._next_states = []
        self._state_pointer = -1

    def __str__(self) -> str:
        new_line = "\n\t"
        child = list(map(str, self._next_states))
        return "Sequential" + super().__str__() + "\n\t" f"{new_line.join(child)}"

    def register_visit(self) -> None:
        """
        Update both the state pointer and visit.
        """
        super().register_visit()
        self._state_pointer += 1

    def get_state(self) -> Location:
        """
        Return the corresponding sub-location object if pointer is in
        the appropriate range.
        """
        if self._state_pointer == -1:
            return self
        if self._state_pointer >= len(self._next_states):
            return self
        try:
            return self._next_states[self._state_pointer]
        except IndexError:
            return self

    def append(self, obj: Location) -> None:
        """
        Add locations in order to the current sequence.
        """
        self._next_states.append(obj)

    def __getitem__(self, index: int) -> Location:
        """
        Shortcut for getting the sub-states
        """
        return self._next_states[index]


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name
        the name of the object.
        - start
        where can the object be found
        if start >= 100, it represents a special location in time too!
        - target
        where can the object be used
        - target_points
        how many points the player will be awarded/punished.

    Representation Invariants:
        - self.name != ""
        - self.target >= -1
        - self.start > 0
    """
    name: str
    start: int
    target: int
    points: int

    def __init__(self, name: str, start: int, target: int, points: int) -> None:
        """Initialize a new item.
        """

        self.name = name
        self.start = start
        self.target = target
        self.points = points

    def __str__(self) -> str:
        return f"Item({self.name=}, {self.start=}, {self.target=}, {self.points=})"

    def __repr__(self) -> str:
        return self.__str__()


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - x
        The horizontal position of the player.
        - y
        The vertical position of the player
        - inventory
        All objects the player currently possess.
        - victory
        If and only if game success victory is true.
        - special_item_conditions
        Conditions on whatever the player can pick certain objects or not.
        - current_moves
        How many moves has the player execute.
        - score
        Player's current score.

    Representation Invariants:
        - self.current_moves >= 0
        - self.x and self.y are in the appropriate range with respect to the world.
    """
    x: int
    y: int
    inventory: list[Item]
    victory: bool
    special_item_conditions: dict[str, bool]
    current_moves: int
    score: int

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False
        self.special_item_conditions = {
            i: False for i in SPECIAL_ITEMS
        }
        for j in FOOD:
            self.special_item_conditions[j] = True
        self.current_moves = 0
        self.score = 0

    def available_directions(self, w: World) -> list[str]:
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """

        max_x = len(w.map[0]) - 1
        max_y = len(w.map) - 1
        location = w.get_location(self.x, self.y)

        direction_option = ["North", "South", "East", "West"]
        p = self

        if location.number != -1:
            return direction_option
        else:
            if p.x == 0:
                direction_option.remove("West")
            if p.x == max_x:
                direction_option.remove("East")
            if p.y == 0:
                direction_option.remove("North")
            if p.y == max_y:
                direction_option.remove("South")

            return direction_option


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: list[list[int]]
        A nested list representation of this world's map
        - locations: dict[int, Location]
        A dictionary maps each number in the map to a location object
        - items: list[Item]
        All items stored. Read from items.txt.
        - visited: list[list[int]]
        A dictionary contains the times visited by the player for every position.

    Representation Invariants:
        - len(self.map) > 0
        - len(self.map[0]) > 0
        - all([len(i) == len(j) for i in self.map for j in self.map])
        - all(num >= 0 for i in j for j in self.visited)
    """
    map: list[list[int]]
    locations: dict[int, Location]
    items: list[Item]
    visited: list[list[int]]

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)
        self.locations = self.load_locations(location_data)
        self.items = self.load_items(items_data)
        self.visited = [[0 for _ in line] for line in self.map]
        self.register_visit(*self.get_origin())

    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """

        return [list(map(int, line.strip().split())) for line in map_data]

    def load_locations(self, location_data: TextIO) -> dict[int, Location]:
        """
        Store locations from open file location_data as a dictionary that maps the location number to its
        corresponding location objects.

        However, location number with 0, 16, -1, and 100 will be handled differently for functionality purposes.

        If the location_data contains lines like:
            LOCATION 3
            Lost and Found
            10
            Short
            Long_1
            Long_2
            Long_3
            END
        then the load_location_data will represent location 3 as
            {3: Location(3, "Lost and Found", "10", "Short", "Long_1\nLong_2\nLong_3", "Normal")}
        """

        locations = {}
        row_locations = location_data.read().split('LOCATION ')[1:]
        for location_text in row_locations:
            information_list = location_text.split("\n")
            number = int(information_list[0])
            name = information_list[1]
            points = int(information_list[2])
            short = information_list[3]
            end_index = information_list.index("END")
            long = "\n".join(information_list[4:end_index])
            if number == 100:
                locations[number] = SequentialLocation(number, name, points, (short, long))
                continue
            locations[number] = Location(number, name, points, (short, long))
            if number > 100:
                locations[100].append(locations[number])
        return locations

    def load_items(self, location_data: TextIO) -> list[Item]:
        """
        Store items from open file location_data as instances of Item class.

        If location_data file contains:
            3 103 5 Friend's Textbook
            4 6 -1 Some Sort Of Food

        Then load_items will assign this world's items list to
        [Item("Friend's Textbook", 3, 103, 5), Item("Some Sort Of Food", 4, 6, -1)]
        """
        items = []
        line = location_data.readline().strip()
        while line != "":
            info = line.split()
            items.append(Item(" ".join(info[3:]), *map(int, info[0:3])))
            line = location_data.readline().strip()
        return items

    def get_pickable_items(self, p: Player) -> list[Item]:
        """
        Return the list of Items avaliable for pickup under the current player's
        status and location.
        """

        result = []
        for i in self.items:
            if not p.special_item_conditions.get(i.name, True):
                continue
            if i.name not in SPECIAL_ITEMS:
                if i.start == self.map[p.y][p.x]:
                    result.append(i)
            elif p.special_item_conditions.get(i.name, ""):
                result.append(i)
        return result

    def get_usable_items(self, p: Player) -> list[Item]:
        """
        Return the list of Items can be used under the player's location.
        """

        result = []
        for i in self.items:
            if i.target == self.map[p.y][p.x]:
                result.append(i)
        return result

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """

        if 0 <= x < len(self.map[0]) and 0 <= y < len(self.map):
            return self.locations[self.map[y][x]]
        return None

    def get_origin(self) -> tuple[int, int]:
        """
        Return the coordinates (x, y) of the origin in the world map.
        """
        m = self.map
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == ORIGIN:
                    return (j, i)
        raise IndexError("Origin Not Found in self.map")

    def register_visit(self, x: int, y: int) -> None:
        """
        Update the self.visited position to be True, for given x and y.
        """
        self.visited[y][x] += 1
        self.get_location(x, y).register_visit()

    def visited_again(self, x: int, y: int) -> bool:
        """
        Returns true iff the location is visited before at least once.
        """
        if self.get_location(x, y).number == 100:
            return False
        return self.visited[y][x] > 1

    def search_item(self, name: str) -> Optional[Item]:
        """
        Returns the item with its corresponding name.
        """
        for i in self.items:
            if i.name == name:
                return i
        return None


class GameState():
    """
    The current state of the game. An instance of the GameState class
    is used to represent all the information of the game at this moment.

    Methods and attributes requiring the composite information of player and
    world will be implemented in this class.

    Instead of w.method(p) or p.method(w), now we can directly gamestate.method().

    Instance Attributes:
        - w
        An instance of the World class which represents the status of the world.
        - p
        An instance of Player class which represents the status of the player.

    """
    w: World
    p: Player

    def __init__(self, w: World, p: Player) -> None:
        self.w = w
        self.p = p

    def save_state(self, name: str = DEFAULT_FILE_NAME) -> None:
        """
        Save the current game to a file.
        By default it is named saved_game_anonymous.pkl.
        """

        with open(f"saved_game_{name}.pkl", "wb") as outp:
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)

    def available_directions(self) -> list[str]:
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """
        # Retrieve the world and player instance from game
        w = self.w
        p = self.p
        max_x = len(w.map[0]) - 1
        max_y = len(w.map) - 1
        location = w.get_location(p.x, p.y)

        direction_option = ["North", "South", "East", "West"]

        if location.number != -1:
            return direction_option
        else:
            if p.x == 0:
                direction_option.remove("West")
            if p.x == max_x:
                direction_option.remove("East")
            if p.y == 0:
                direction_option.remove("North")
            if p.y == max_y:
                direction_option.remove("South")

            return direction_option

    def move(self, direction: str, step: int = 1) -> bool:
        """
        Move the player to the given direction by given steps. If less steps are elligible
        than the step parameter, execution will stop after executing the last legal step.

        If the given direction is not avaliable at the beginning, False will be returned and
        nothing will be executed. Otherwise, return True.

        Precondition:
        - direction.lower() in DIRECTIONS
        - step >= 1
        """
        w = self.w
        p = self.p

        command = direction[0].upper() + direction[1:].lower()
        if direction.lower() not in DIRECTIONS:
            return False

        if command in self.available_directions():

            current_score = p.score

            if command == "West":
                p.x -= 1
            if command == "East":
                p.x += 1
            if command == "North":
                p.y -= 1
            if command == "South":
                p.y += 1
            w.register_visit(p.x, p.y)

            new_location = w.get_location(p.x, p.y)
            if new_location:
                if w.visited[p.y][p.x] == 1 and new_location.points != 0:  # Case for updating the score
                    p.score += new_location.points
                    print(f"Score updated: {current_score} -> {p.score}")

            if len(self.available_directions()) < 4:
                print(LOCATION_WARNING)
            if step > 1:
                self.move(direction, step - 1)
                return True
            return True
        return False

    def pick_up_item(self, item_name: str) -> None:
        """
        Handles picking up an item by name. Updates the player's inventory and score.
        """
        # Find the item by name
        item = next((obj for obj in self.w.items if obj.name.lower() == item_name.lower()), None)

        if item and item not in self.p.inventory:
            self.p.inventory.append(item)  # Add item to the player's inventory
            self.p.score += item.points  # Update the player's score with the item's points
            print(f"{item.name} added to your inventory. "
                  f"\nScore increased by {item.points}. Current score: {self.p.score}")
        else:
            print(f"Item {item_name} not found or already in inventory.")

    @staticmethod
    def restore_state(name: str = DEFAULT_FILE_NAME) -> GameState:
        """
        Load the game with respect to the corresponding input name.
        """

        with open(f"saved_game_{name}.pkl", "rb") as intp:
            restored = pickle.load(intp)
        return restored

    @staticmethod
    def get_current_saved_files() -> list[str]:
        """
        Get all restorable game files under the current directory.
        """

        return [f.split("_")[2].removesuffix(".pkl")
                for f in os.listdir(os.getcwd()) if f.endswith(".pkl")
                ]

