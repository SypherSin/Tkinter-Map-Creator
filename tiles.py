class Tiles:
    def __init__(self, symbol, name, description, type, walkable, passable, enter, color):
        self.symbol = symbol
        self.name = name
        self.description = description
        self.type = type
        self.walkable = walkable
        self.passable = passable
        self.enter = enter
        self.color = color

trial = Tiles(".", "Trail", "Usually a good place to walk", "Ground", True, True, False, "green")
water = Tiles("~", "Water", "Go for a swim?", "Liquid", True, True, False, "blue")
mountain = Tiles("^", "Mountain", "Cannot Pass", "Ground", False, False, False, "grey")
store = Tiles("s", "Store", "Don't go away just yet", "Merchant", True, False, True, "gold")
empty = Tiles("e", "Empty Tile", "Put something here", "Blank", False, False, False, "grey30")

map_1_to_2 = Tiles("1_2_1", "Transfer", "Move to map 2", "Transfer", True, True, True, "black")

character_tile = Tiles("H", "Character", "Your character", "Character", True, True, False, "red")

terrain_tiles = [trial, water, mountain, empty]
interaction_tiles = [store]
transfer_tiles = [map_1_to_2]