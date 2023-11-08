import tkinter as tk
from tkinter import ttk  # Import ttk for Treeview widget
import clipboard
import json

SAVED_DATA = "clipboard.json"

def save_data(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f)

def load_data(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except:
        return {}

def save_clipboard_data():
    key = key_entry.get()
    data[key] = clipboard.paste()
    save_data(SAVED_DATA, data)
    status_label.config(text="Data saved!")

def load_clipboard_data():
    key = key_entry.get()
    if key in data:
        clipboard.copy(data[key])
        status_label.config(text="Data copied to clipboard.")
    else:
        status_label.config(text="Key does not exist.")

def list_clipboard_data():
    # Clear the existing table
    for item in tree.get_children():
        tree.delete(item)

    # Populate the table with clipboard data
    for key, value in data.items():
        tree.insert("", "end", values=(key, value))

data = load_data(SAVED_DATA)

# Create the main window
root = tk.Tk()
root.title("Clipboard Manager")

# Create and configure GUI elements
key_label = tk.Label(root, text="Enter a key:")
key_entry = tk.Entry(root)
save_button = tk.Button(root, text="Save", command=save_clipboard_data)
load_button = tk.Button(root, text="Load", command=load_clipboard_data)
list_button = tk.Button(root, text="List", command=list_clipboard_data)
status_label = tk.Label(root, text="")

# Create a Treeview widget for the table
tree = ttk.Treeview(root, columns=("Key", "Value"), show="headings")
tree.heading("Key", text="Key")
tree.heading("Value", text="Value")

# Place GUI elements in the window
key_label.pack()
key_entry.pack()
save_button.pack()
load_button.pack()
list_button.pack()
status_label.pack()
tree.pack()  # Add the Treeview to the window

root.mainloop()
