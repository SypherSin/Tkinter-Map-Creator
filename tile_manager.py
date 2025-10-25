selected_tile = None  # Variable to hold the currently selected tile

def set_selected_tile(tile_symbol):
    global selected_tile
    selected_tile = tile_symbol
    print(f"Selected tile set to: {selected_tile}")  # Debug statement

def get_selected_tile():
    return selected_tile

def clear_selected_tile():
    global selected_tile
    selected_tile = None
    print("Selected tile cleared.")  # Debug statement