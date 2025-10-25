import importlib
import os

def load_map(map_name):
    try:
        module = importlib.import_module(f'maps.{map_name}')
        layout_variable_name = f'map_layout_{map_name.split("_")[1]}'
        map_layout = getattr(module, layout_variable_name)
        return map_layout
    except (ImportError, AttributeError) as e:
        print(f"Error loading map: {e}")
        return None

def get_tile_color(tile_symbol, terrain_tiles, interaction_tiles, transfer_tiles):
    for tile in terrain_tiles + interaction_tiles + transfer_tiles:
        if tile.symbol == tile_symbol:
            return tile.color
    return "white"  # Default color for unknown tiles