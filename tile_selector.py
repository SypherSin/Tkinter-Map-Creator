import tkinter as tk
from tiles import terrain_tiles, interaction_tiles, transfer_tiles
from tile_manager import set_selected_tile  # Import the function

def open_tile_selection():
    tile_window = tk.Toplevel()
    tile_window.title("Select Tile")
    tile_window.configure(background="blue")

    for index, tile in enumerate(terrain_tiles + interaction_tiles + transfer_tiles):
        button = tk.Button(tile_window, text=tile.name, command=lambda t=tile: select_tile(t, tile_window), width=30)
        button.grid(row=index, column=0, padx=10, pady=1)

def select_tile(tile, tile_window):
    set_selected_tile(tile.symbol)  # Use the tile_manager to set the selected tile
    tile_window.destroy()  # Close the tile selection window