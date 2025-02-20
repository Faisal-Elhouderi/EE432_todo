import tkinter as tk
from tkinter import ttk, messagebox

from todo_list import ToDoList

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.todo_list = ToDoList()

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Entry Frame
        entry_frame = ttk.Frame(self.root, padding="10")
        entry_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Label(entry_frame, text="Description:").grid(row=0, column=0, sticky=tk.W)
        self.description_entry = ttk.Entry(entry_frame, width=30)
        self.description_entry.grid(row=0, column=1, padx=5)

        ttk.Label(entry_frame, text="Priority:").grid(row=1, column=0, sticky=tk.W)
        self.priority_combo = ttk.Combobox(entry_frame, values=["High", "Medium", "Low"], state="readonly")
        self.priority_combo.grid(row=1, column=1, padx=5)

        self.status_var = tk.BooleanVar()
        self.status_check = ttk.Checkbutton(entry_frame, text="Completed", variable=self.status_var)
        self.status_check.grid(row=2, column=1, sticky=tk.W, pady=5)

        ttk.Button(entry_frame, text="Add Task", command=self.add_task).grid(row=3, column=1, pady=5, sticky=tk.E)

        # Action Frame
        action_frame = ttk.Frame(self.root, padding="10")
        action_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))

        ttk.Button(action_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="Search Task", command=self.search_task).grid(row=0, column=1, padx=5)
        ttk.Button(action_frame, text="Show All", command=lambda: self.display_tasks()).grid(row=0, column=2, padx=5)
        ttk.Button(action_frame, text="Show by Priority", command=lambda: self.display_tasks('priority')).grid(row=0, column=3, padx=5)
        ttk.Button(action_frame, text="Show Completed", command=lambda: self.display_filtered(True)).grid(row=0, column=4, padx=5)
        ttk.Button(action_frame, text="Show Pending", command=lambda: self.display_filtered(False)).grid(row=0, column=5, padx=5)

        # Display Frame
        display_frame = ttk.Frame(self.root, padding="10")
        display_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))

        self.tree = ttk.Treeview(display_frame, columns=("Description", "Priority", "Status"), show="headings")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.column("Description", width=200)
        self.tree.column("Priority", width=100)
        self.tree.column("Status", width=100)
        self.tree.pack()

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        entry_frame.columnconfigure(1, weight=1)

    def add_task(self):
        description = self.description_entry.get()
        priority = self.priority_combo.get()
        status = self.status_var.get()
        if not description or not priority:
            messagebox.showerror("Error", "Description and Priority are required.")
            return
        success = self.todo_list.add_task(description, priority, status)
        if success:
            self.description_entry.delete(0, tk.END)
            self.priority_combo.set('')
            self.status_var.set(False)
            self.display_tasks()
            messagebox.showinfo("Success", "Task added successfully.")
        else:
            messagebox.showerror("Error", "Task with this description already exists.")

    def delete_task(self):
        description = self.description_entry.get()
        if not description:
            messagebox.showerror("Error", "Description is required to delete a task.")
            return
        success = self.todo_list.delete_task(description)
        if success:
            self.display_tasks()
            messagebox.showinfo("Success", "Task deleted successfully.")
        else:
            messagebox.showerror("Error", "Task not found.")

    def search_task(self):
        description = self.description_entry.get()
        task = self.todo_list.search_task(description)
        if task:
            messagebox.showinfo("Task Found", f"Description: {task.description}\nPriority: {task.priority_str}\nStatus: {'Completed' if task.status else 'Pending'}")
        else:
            messagebox.showerror("Error", "Task not found.")

    def display_tasks(self, sort_by='insertion'):
        tasks = self.todo_list.display_tasks(sort_by)
        self._update_treeview(tasks)

    def display_filtered(self, status):
        tasks = self.todo_list.display_filtered(status)
        self._update_treeview(tasks)

    def _update_treeview(self, tasks):
        self.tree.delete(*self.tree.get_children())
        for task in tasks:
            status = 'Completed' if task.status else 'Pending'
            self.tree.insert("", "end", values=(task.description, task.priority_str, status))

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()