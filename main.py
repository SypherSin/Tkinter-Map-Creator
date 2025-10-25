import tkinter as tk
import os
import importlib
from tkinter import messagebox
from map_editor import create_map  # Use the unified module

# Global variable to keep track of the current map layout
current_map_layout = None

def main():
    menu_window = tk.Tk()  # Create the main menu window
    menu_window.title("Map Editor")  # Set the title for the window
    menu_window.configure(background="blue")

    # Create a label
    label = tk.Label(menu_window, text="Main Menu", font=30, width=30)
    label.grid(row=0, column=0, padx=10, pady=10)  # Position the label in the grid

    # Create buttons for loading and saving maps
    load_button = tk.Button(menu_window, text="Load Map", command=load_map, width=30)
    load_button.grid(row=1, column=0, padx=10, pady=1)

    save_button = tk.Button(menu_window, text="Save Map", command=save_map_dialog, width=30)
    save_button.grid(row=2, column=0, padx=10, pady=1)

    # Create a button to submit the input
    submit_button = tk.Button(menu_window, text="Exit", command=menu_window.destroy, width=30)
    submit_button.grid(row=3, column=0, padx=10, pady=10)  # Position the submit button

    global current_map_layout
    current_map_layout = []  # Start with an empty layout

    menu_window.mainloop()

def load_map():
    load_window = tk.Toplevel()
    load_window.title("Select Map File")
    load_window.configure(background="blue")
    
    map_folder = os.path.join(os.getcwd(), 'Map Creator/maps')
    
    if not os.path.exists(map_folder):
        messagebox.showerror("Error", f"The folder '{map_folder}' does not exist.")
        load_window.destroy()
        return

    map_files = [f for f in os.listdir(map_folder) if f.endswith('.py') and f.startswith('map_')]
    
    if not map_files:
        messagebox.showinfo("No Maps Found", "No map files found in the maps folder.")
        load_window.destroy()
        return

    for index, map_file in enumerate(map_files):
        map_name = map_file[:-3]
        button = tk.Button(load_window, text=map_name, command=lambda mf=map_name: on_load(mf, load_window), width=30)
        button.grid(row=index, column=0, padx=10, pady=1)

    load_window.transient()  # Set as a transient window
    load_window.grab_set()  # Make it modal

def on_load(selected_file, load_window):
    try:
        module = importlib.import_module(f'maps.{selected_file}')
        global current_map_layout
        
        map_number = selected_file.split('_')[1][0]
        layout_variable_name = f'map_layout_{map_number}'
        current_map_layout = getattr(module, layout_variable_name)

        if current_map_layout is None:
            raise ValueError("Loaded map layout is None.")

        print("Map loaded.")
        
        # Create a new top-level window for the map editor
        print("Creating map editor window...")
        map_editor_window = tk.Toplevel()
        map_editor_window.title("Map Editor")
        create_map(map_editor_window, current_map_layout)  # Pass layout to create_map
        
        load_window.destroy()
    except (ImportError, AttributeError, ValueError) as e:
        messagebox.showerror("Error", f"Failed to load the selected map. Error: {e}")

def save_map_dialog():
    save_window = tk.Toplevel()
    save_window.title("Save Map")

    map_folder = os.path.join(os.getcwd(), 'Map Creator/maps')
    map_files = [f for f in os.listdir(map_folder) if f.endswith('.py') and f.startswith('map_')]

    # Existing maps
    for index, map_file in enumerate(map_files):
        map_name = map_file[:-3]
        button = tk.Button(save_window, text=f"Overwrite {map_name}", command=lambda mf=map_name: save_map(mf, save_window))
        button.grid(row=index, column=0, padx=10, pady=5)

    # Option to create a new map
    tk.Label(save_window, text="Or create a new map:").grid(row=len(map_files), column=0, padx=10, pady=5)
    new_map_name_entry = tk.Entry(save_window)
    new_map_name_entry.grid(row=len(map_files) + 1, column=0, padx=10, pady=5)

    save_button = tk.Button(save_window, text="Save New Map", command=lambda: save_map(new_map_name_entry.get(), save_window))
    save_button.grid(row=len(map_files) + 2, column=0, padx=10, pady=5)

def save_map(map_name, save_window):
    global current_map_layout
    if current_map_layout is None:
        messagebox.showwarning("No Map Loaded", "Please load a map before saving.")
        save_window.destroy()
        return
    
    # Create the full file path
    file_path = os.path.join(os.getcwd(), 'Map Creator/maps', f"{map_name}.py")
    
    # Write the map layout with proper formatting
    with open(file_path, "w") as f:
        f.write("from tiles import terrain_tiles, interaction_tiles\n\n")
        f.write(f"map_layout_{map_name[-1]} = [\n")  # Assuming map_name ends with a number
        for row in current_map_layout:
            f.write("    " + repr(row) + ",\n")  # Write each row with formatting
        f.write("]\n")  # Close the map layout list
    print("Map saved as:", map_name)
    save_window.destroy()

if __name__ == "__main__":
    main()