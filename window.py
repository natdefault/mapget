import tkinter as tk
from tkinter import ttk
from manager import MappingManager


class AppWindow:
    def __init__(self):
        self.manager = MappingManager()

        self.root = tk.Tk()
        self.root.title("MapGet Tool")
        self.root.geometry("700x400")

        self.input_label = tk.Label(self.root, text="Enter query:")
        self.input_label.pack()

        self.input_box = tk.Entry(self.root, width=80)
        self.input_box.pack()

        self.mapping_type = ttk.Combobox(
            self.root,
            values=["auto", "yarn", "mojmap", "mcp", "obfuscated"],
            state="readonly"
        )
        self.mapping_type.set("auto")
        self.mapping_type.pack()

        self.version_box = tk.Entry(self.root, width=20)
        self.version_box.insert(0, "1.20.1")
        self.version_box.pack()

        self.button = tk.Button(self.root, text="Search", command=self.search)
        self.button.pack()

        self.output = tk.Text(self.root, height=15)
        self.output.pack()

    def search(self):
        query = self.input_box.get()
        mapping = self.mapping_type.get()
        version = self.version_box.get()

        result = self.manager.handle_query(query, mapping, version)

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, result)

    def run(self):
        self.root.mainloop()