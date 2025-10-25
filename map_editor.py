import tkinter as tk
from tiles import terrain_tiles, interaction_tiles, transfer_tiles
from tile_manager import get_selected_tile
from tile_selector import open_tile_selection  # Import the tile selection function

# Global variables
tile_size = 37
map_layout = []  # Initialize as empty
canvas = None  # Reference to the canvas

def create_map(master, layout):
    global canvas, map_layout
    map_layout = layout
    rows = len(layout)
    cols = len(layout[0]) if rows > 0 else 0

    # Create a new window for controls
    control_window = tk.Toplevel(master)
    control_window.title("Map Controls")

    # Control buttons
    tile_button = tk.Button(control_window, text="Select Tile", command=open_tile_selection)
    tile_button.grid(row=0, column=0, padx=10, pady=10)

    increase_row_button = tk.Button(control_window, text="Add Row", command=lambda: adjust_map_size(1, 0))
    increase_row_button.grid(row=0, column=1, padx=10, pady=5)

    decrease_row_button = tk.Button(control_window, text="Remove Row", command=lambda: adjust_map_size(-1, 0))
    decrease_row_button.grid(row=0, column=2, padx=10, pady=5)

    increase_col_button = tk.Button(control_window, text="Add Column", command=lambda: adjust_map_size(0, 1))
    increase_col_button.grid(row=0, column=3, padx=10, pady=5)

    decrease_col_button = tk.Button(control_window, text="Remove Column", command=lambda: adjust_map_size(0, -1))
    decrease_col_button.grid(row=0, column=4, padx=10, pady=5)

    # Create a frame for the canvas and scroll bars
    frame = tk.Frame(master)
    frame.grid(row=1, column=0, sticky="nsew")

    # Configure grid weights for resizing
    master.grid_rowconfigure(1, weight=1)  # Allow the frame to expand vertically
    master.grid_columnconfigure(0, weight=1)  # Allow the frame to expand horizontally
    frame.grid_columnconfigure(0, weight=1)  # Allow the canvas to expand horizontally
    frame.grid_rowconfigure(0, weight=1)  # Allow the canvas to expand vertically

    # Create scroll bars
    vertical_scrollbar = tk.Scrollbar(frame, orient="vertical")
    vertical_scrollbar.grid(row=0, column=1, sticky="ns")

    horizontal_scrollbar = tk.Scrollbar(frame, orient="horizontal")
    horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

    # Create the canvas for the map
    canvas = tk.Canvas(frame, bg="white", width=cols * tile_size, height=rows * tile_size,
                       yscrollcommand=vertical_scrollbar.set,
                       xscrollcommand=horizontal_scrollbar.set)
    canvas.grid(row=0, column=0, sticky="nsew")

    # Configure scroll bars
    vertical_scrollbar.config(command=canvas.yview)
    horizontal_scrollbar.config(command=canvas.xview)

    # Create a frame inside the canvas to hold the map
    map_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=map_frame, anchor="nw")

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    map_frame.bind("<Configure>", update_scrollregion)

    # Bind click event to place tiles
    canvas.bind("<Button-1>", place_tile)  # Bind left mouse click to place_tile function

    draw_map()  # Draw the map initially

def place_tile(event):
    global map_layout
    tile_size = 37  # Ensure this matches your defined tile size
    col = event.x // tile_size
    row = event.y // tile_size
    
    if 0 <= col < len(map_layout[0]) and 0 <= row < len(map_layout):
        selected_tile_symbol = get_selected_tile()  # Get the currently selected tile symbol
        map_layout[row][col] = selected_tile_symbol  # Update the map layout
        draw_map()  # Redraw the map to show the new tile

def adjust_map_size(row_change, col_change):
    global map_layout
    if row_change > 0:  # Add row
        map_layout.append([None] * len(map_layout[0]))  # Add a new row with empty tiles
    elif row_change < 0 and len(map_layout) > 0:  # Remove row
        map_layout.pop()
    
    if col_change > 0:  # Add column
        for row in map_layout:
            row.append(None)  # Add a new column with empty tiles
    elif col_change < 0 and len(map_layout) > 0:  # Remove column
        for row in map_layout:
            row.pop()

    draw_map()  # Redraw the map after changes

def draw_map():
    global canvas, map_layout
    canvas.delete("all")
    for row_index, row in enumerate(map_layout):
        for col_index, tile in enumerate(row):
            tile_color = "gray"  # Default color for empty tiles
            if tile is not None:
                for t in terrain_tiles + interaction_tiles + transfer_tiles:
                    if t.symbol == tile:
                        tile_color = t.color  # Set color based on tile symbol
                        break
            x0 = col_index * tile_size
            y0 = row_index * tile_size
            canvas.create_rectangle(x0, y0, x0 + tile_size, y0 + tile_size, fill=tile_color)
    # Update the scroll region after drawing the map
    canvas.configure(scrollregion=canvas.bbox("all"))
    print("Map drawn.")