import mysql.connector
import tkinter as tk
from tkinter import messagebox

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="task_manager"
)
cursor = db.cursor()

# Function to create a new task
def create_task(title, description):
    sql = "INSERT INTO tasks (title, description) VALUES (%s, %s)"
    values = (title, description)
    cursor.execute(sql, values)
    db.commit()
    messagebox.showinfo("Success", "Task created successfully.")
    read_tasks()  # Refresh task list after adding

# Function to read all tasks
def read_tasks():
    task_list.delete(0, tk.END)  # Clear the listbox
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    if not tasks:
        messagebox.showinfo("Info", "No tasks found.")
    else:
        for task in tasks:
            status = "Completed" if task[3] else "Not Completed"
            task_list.insert(tk.END, f"{task[0]} - {task[1]} ({status})")

# Function to mark a task as completed
def complete_task():
    try:
        task_index = task_list.curselection()[0]
        task_id = int(task_list.get(task_index).split()[0])  # Extract task ID
        sql = "UPDATE tasks SET completed = TRUE WHERE id = %s"
        cursor.execute(sql, (task_id,))
        db.commit()
        messagebox.showinfo("Success", f"Task with ID {task_id} marked as completed.")
        read_tasks()  # Refresh task list after completion
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark as completed.")

# Function to delete a task
def delete_task():
    try:
        task_index = task_list.curselection()[0]
        task_id = int(task_list.get(task_index).split()[0])  # Extract task ID
        sql = "DELETE FROM tasks WHERE id = %s"
        cursor.execute(sql, (task_id,))
        db.commit()
        messagebox.showinfo("Success", f"Task with ID {task_id} deleted.")
        read_tasks()  # Refresh task list after deletion
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete.")

# Function to handle the 'Add Task' button click
def add_task():
    title = title_entry.get()
    description = description_entry.get("1.0", tk.END).strip()
    
    if title and description:
        create_task(title, description)
        title_entry.delete(0, tk.END)
        description_entry.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter both title and description.")

# GUI Setup
root = tk.Tk()
root.title("Task Manager")

# Create GUI elements with improved layout and styling
title_label = tk.Label(root, text="Title:", font=("Arial", 12))
title_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

title_entry = tk.Entry(root, width=50, font=("Arial", 12))
title_entry.grid(row=0, column=1, padx=10, pady=5)

description_label = tk.Label(root, text="Description:", font=("Arial", 12))
description_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

description_entry = tk.Text(root, width=50, height=4, font=("Arial", 12))
description_entry.grid(row=1, column=1, padx=10, pady=5)

add_button = tk.Button(root, text="Add Task", width=20, command=add_task, font=("Arial", 12))
add_button.grid(row=2, column=0, columnspan=2, pady=10)

task_list = tk.Listbox(root, width=60, height=10, font=("Arial", 12))
task_list.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

read_tasks()  # Initial task list load

complete_button = tk.Button(root, text="Mark as Completed", width=20, command=complete_task, font=("Arial", 12))
complete_button.grid(row=4, column=0, pady=10)

delete_button = tk.Button(root, text="Delete Task", width=20, command=delete_task, font=("Arial", 12))
delete_button.grid(row=4, column=1, pady=10)

# Close database connection on window close
def on_closing():
    db.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
