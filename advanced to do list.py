import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
import os

class TodoList:
    def __init__(self, filename='tasks.txt'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                tasks = []
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.rsplit(' | ', 3)
                        if len(parts) == 4:
                            task, completed, priority, due_date = parts
                            tasks.append({
                                'task': task,
                                'completed': completed == 'True',
                                'priority': priority,
                                'due_date': due_date
                            })
            return tasks
        return []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            for task in self.tasks:
                file.write(f"{task['task']} | {task['completed']} | {task['priority']} | {task['due_date']}\n")
        print("Tasks saved to file.")

    def add_task(self, task, priority, due_date):
        self.tasks.append({'task': task, 'completed': False, 'priority': priority, 'due_date': due_date})
        self.save_tasks()

    def remove_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks.pop(task_index)
            self.save_tasks()

    def complete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index]['completed'] = True
            self.save_tasks()

    def edit_task(self, task_index, new_task, new_priority, new_due_date):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].update({
                'task': new_task,
                'priority': new_priority,
                'due_date': new_due_date
            })
            self.save_tasks()

    def filter_tasks(self, completed):
        return [task for task in self.tasks if task['completed'] == completed]

    def search_tasks(self, keyword):
        return [task for task in self.tasks if keyword.lower() in task['task'].lower()]

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced To-Do List")
        self.root.geometry("600x750")

        self.style = ttk.Style()
        self.is_dark_mode = True  # Start in dark mode

        self.todo_list = TodoList()
        self.task_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.due_date_var = tk.StringVar()

        self.create_widgets()
        self.update_styles()  # Apply styles after creating widgets
        self.update_task_list()

    def create_widgets(self):
        ttk.Label(self.root, text="Unique To-Do List", font=("Arial", 18)).pack(pady=20)

        # Task input area
        ttk.Label(self.root, text="Task:").pack(pady=10)
        self.task_text = tk.Text(self.root, height=5, width=70)
        self.task_text.pack(pady=5)

        # Priority input
        ttk.Label(self.root, text="Priority (High, Medium, Low):").pack(pady=10)
        ttk.Entry(self.root, textvariable=self.priority_var, width=70).pack(pady=5)

        # Due date input
        ttk.Label(self.root, text="Due Date (DD-MM-YYYY):").pack(pady=10)
        ttk.Entry(self.root, textvariable=self.due_date_var, width=70).pack(pady=5)

        # Action buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Complete Task", command=self.complete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Task", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Task", command=self.remove_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Filter Completed", command=self.filter_completed).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search Task", command=self.search_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All Tasks", command=self.clear_all_tasks).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Toggle Dark/Light Mode", command=self.toggle_mode).pack(side=tk.LEFT, padx=5)

        # Task display area
        self.task_listbox = tk.Listbox(self.root, width=75, height=20, font=("Arial", 12))
        self.task_listbox.pack(pady=10)
        self.task_listbox.bind("<Double-1>", self.on_task_double_click)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.task_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        # Status bar
        self.status_bar = ttk.Label(self.root, text="", relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_task_double_click(self, event):
        self.edit_task()

    def toggle_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_styles()

    def update_styles(self):
        if self.is_dark_mode:
            self.root.configure(bg="#2c2c2c")
            self.style.configure("TButton", background="#ffcc00", foreground="black")
            self.style.configure("TLabel", background="#2c2c2c", foreground="white")
            self.style.configure("TEntry", background="#383838", foreground="white")
            self.task_listbox.configure(bg="#383838", fg="white", selectbackground="#61afef")
            self.status_bar.configure(background="#2c2c2c", foreground="white")
        else:
            self.root.configure(bg="white")
            self.style.configure("TButton", background="#cccccc", foreground="black")
            self.style.configure("TLabel", background="white", foreground="black")
            self.style.configure("TEntry", background="lightgrey", foreground="black")
            self.task_listbox.configure(bg="white", fg="black", selectbackground="#61afef")
            self.status_bar.configure(background="white", foreground="black")

    def add_task(self):
        task = self.task_text.get("1.0", tk.END).strip()
        priority = self.priority_var.get().strip()
        due_date = self.due_date_var.get().strip()

        valid_priorities = ['High', 'Medium', 'Low']
        if task and priority in valid_priorities and due_date:
            if self.validate_due_date(due_date):
                self.todo_list.add_task(task, priority, due_date)
                self.update_task_list()
                self.clear_entries()
                self.update_status("Task added successfully.")
            else:
                messagebox.showwarning("Warning", "Due date must be in DD-MM-YYYY format and not in the past.")
        else:
            messagebox.showwarning("Warning", "You must enter a valid task, priority (High, Medium, Low), and due date.")

    def validate_due_date(self, due_date):
        try:
            date = datetime.strptime(due_date, '%d-%m-%Y')
            return date >= datetime.now()
        except ValueError:
            return False

    def complete_task(self):
        self.modify_task(self.todo_list.complete_task)

    def edit_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task = self.todo_list.tasks[selected_index]

            new_task = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=task['task'])
            new_priority = simpledialog.askstring("Edit Priority", "Edit priority (High, Medium, Low):", initialvalue=task['priority'])
            new_due_date = simpledialog.askstring("Edit Due Date", "Edit due date:", initialvalue=task['due_date'])

            valid_priorities = ['High', 'Medium', 'Low']
            if new_task and new_priority in valid_priorities and new_due_date:
                if self.validate_due_date(new_due_date):
                    self.todo_list.edit_task(selected_index, new_task, new_priority, new_due_date)
                    self.update_task_list()
                    self.update_status("Task edited successfully.")
                else:
                    messagebox.showwarning("Warning", "Due date must be in DD-MM-YYYY format and not in the past.")
            else:
                messagebox.showwarning("Warning", "You must enter a valid task, priority, and due date.")
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to edit.")

    def remove_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            if messagebox.askyesno("Confirm", "Are you sure you want to remove this task?"):
                self.todo_list.remove_task(selected_index)
                self.update_task_list()
                self.update_status("Task removed successfully.")
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to remove.")

    def clear_all_tasks(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.todo_list.tasks.clear()
            self.todo_list.save_tasks()
            self.update_task_list()
            self.update_status("All tasks cleared.")

    def modify_task(self, modify_function):
        try:
            selected_index = self.task_listbox.curselection()[0]
            modify_function(selected_index)
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task.")

    def filter_completed(self):
        completed_tasks = self.todo_list.filter_tasks(True)
        self.display_tasks(completed_tasks)
        self.update_status("Showing completed tasks.")

    def search_task(self):
        keyword = simpledialog.askstring("Search Task", "Enter keyword to search:")
        if keyword:
            self.display_tasks(self.todo_list.search_tasks(keyword))
            self.update_status(f"Showing search results for: {keyword}")

    def update_task_list(self):
        self.display_tasks(self.todo_list.tasks)
        self.update_status(f"Total tasks: {len(self.todo_list.tasks)}")

    def display_tasks(self, tasks):
        self.task_listbox.delete(0, tk.END)
        for task in tasks:
            status = "✓" if task['completed'] else "✗"
            display_text = f"[{status}] {task['task']} | {task['priority']} | Due: {task['due_date']}"
            self.task_listbox.insert(tk.END, display_text)

            # Color based on completion
            if task['completed']:
                self.task_listbox.itemconfig(tk.END, {'bg': '#4CAF50', 'fg': 'white'})  # Green for completed
            else:
                self.task_listbox.itemconfig(tk.END, {'bg': '#FFCDD2', 'fg': 'black'})  # Light red for pending

    def clear_entries(self):
        self.task_text.delete("1.0", tk.END)
        self.priority_var.set("")
        self.due_date_var.set("")

    def update_status(self, message):
        self.status_bar.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
