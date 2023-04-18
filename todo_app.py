import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import os.path
import sys
from datetime import datetime, timedelta

if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    script_dir = os.path.dirname(os.path.realpath(__file__))

DATA_FILE = os.path.join(script_dir, "todo_data.json")

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List App")
        self.root.attributes('-topmost', True)
        self.todo_items = []
        self.load_data()
        self.build_gui()

	def build_gui(self):
		self.frame = tk.Frame(self.root, padx=10, pady=10)
		self.frame.pack(fill=tk.BOTH, expand=True)

		self.item_container = tk.Frame(self.frame)
		self.item_container.pack(fill=tk.BOTH, expand=True)

		self.entry = tk.Entry(self.frame, font=("Helvetica", 14))
		self.entry.pack(fill=tk.X, pady=(10, 5))

		# Bind the "Return" key press event to the add_item method
		self.entry.bind('<Return>', lambda event: self.add_item())

		self.add_button = tk.Button(self.frame, text="Add Item", font=("Helvetica", 16), command=self.add_item)
		self.add_button.pack(fill=tk.X, pady=(0, 10))

		self.render_list()


    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self.todo_items = json.load(f)
        else:
            self.todo_items = []

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.todo_items, f)

    def add_item(self):
        item_text = self.entry.get()
        if item_text:
            new_item = {
                "text": item_text,
                "completed": False,
                "timestamp": None
            }
            self.todo_items.append(new_item)
            self.save_data()
            self.render_list()
            self.entry.delete(0, tk.END)

    def complete_item(self, index):
        item = self.todo_items[index]
        if item["completed"]:
            result = messagebox.askyesno("Confirmation", "Do you want to mark this item as unfinished?")
            if result:
                item["completed"] = False
                item["timestamp"] = None
                self.save_data()
                self.render_list()
        else:
            item["completed"] = True
            item["timestamp"] = datetime.now().isoformat()
            self.save_data()
            self.render_list()

    def delete_item(self, index):
        print(f"calling delete_item({index}")
        result = messagebox.askyesno("Confirmation", "Do you want to delete this item?")
        if result:
            print(f"Deleting item {index}")
            del self.todo_items[index]
            self.save_data()
            self.render_list()

	def render_list(self):
		for widget in self.item_container.winfo_children():
			widget.destroy()

		# Sort the items based on their completion status
		sorted_items = sorted(self.todo_items, key=lambda x: x["completed"])

		for i, item in enumerate(sorted_items):
			text = item["text"]
			completed_time = datetime.fromisoformat(item["timestamp"]) if item["timestamp"] else None
			remaining_time = None

			if item["completed"] and completed_time:
				remaining_time = timedelta(hours=24) - (datetime.now() - completed_time)
				if remaining_time <= timedelta(0):
					continue
				hours_remaining = int(remaining_time.total_seconds() // 3600)
				text = f"✓ {text} ({hours_remaining}h)"

			label = tk.Label(self.item_container, text=text, font=("Helvetica", 14), padx=5, pady=5)

			if item["completed"]:
				label.config(fg="gray", font=("Helvetica", 14, "overstrike"))

			label.grid(row=i, column=0, sticky=tk.W)

			label.bind('<Button-1>', lambda event, index=i: self.complete_item(index))
			label.bind('<Button-3>', lambda event, index=i: self.delete_item(index))
			label.bind('<Button-2>', lambda event, index=i: self.delete_item(index))


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
