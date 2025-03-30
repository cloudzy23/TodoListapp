import tkinter as tk
from tkinter import simpledialog
import json
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import pandas as pd
import numpy as np

class NimbusTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nimbus Todo List")
        self.root.geometry("500x450")
        self.root.configure(bg="#f5f5f5")
        
        self.current_user = None
        self.user_data = {}
        self.load_user_data()
        
        # Set up the frames
        self.auth_frame = tk.Frame(root, bg="#f5f5f5")
        self.todo_frame = tk.Frame(root, bg="#f5f5f5")
        self.analytics_frame = tk.Frame(root, bg="#f5f5f5")
        
        self.setup_auth_frame()
        self.setup_todo_frame()
        self.setup_analytics_frame()
        
        # Initially show auth frame
        self.auth_frame.pack(fill=tk.BOTH, expand=True)
    
    def load_user_data(self):
        if os.path.exists("nimbus_users.json"):
            try:
                with open("nimbus_users.json", "r") as file:
                    self.user_data = json.load(file)
            except:
                self.user_data = {}
    
    def save_user_data(self):
        with open("nimbus_users.json", "w") as file:
            json.dump(self.user_data, file)
    
    def setup_auth_frame(self):
        # Header
        tk.Label(
            self.auth_frame, 
            text="Your Personal Nimbus Todo List", 
            font=("Arial", 16, "bold"),
            bg="#f5f5f5",
            pady=10
        ).pack()
        
        # Name entry
        tk.Label(
            self.auth_frame, 
            text="Please enter your name:", 
            font=("Arial", 12),
            bg="#f5f5f5",
            pady=5
        ).pack()
        
        self.name_entry = tk.Entry(self.auth_frame, font=("Arial", 12), width=30)
        self.name_entry.pack(pady=5)
        
        # Password entry
        tk.Label(
            self.auth_frame, 
            text="Password:", 
            font=("Arial", 12),
            bg="#f5f5f5",
            pady=5
        ).pack()
        
        self.password_entry = tk.Entry(self.auth_frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack(pady=5)
        
        # Feedback label
        self.auth_feedback = tk.Label(
            self.auth_frame, 
            text="", 
            font=("Arial", 10),
            bg="#f5f5f5",
            fg="red",
            pady=5
        )
        self.auth_feedback.pack()
        
        # Buttons frame
        buttons_frame = tk.Frame(self.auth_frame, bg="#f5f5f5")
        buttons_frame.pack(pady=20)
        
        tk.Button(
            buttons_frame,
            text="Register",
            font=("Arial", 12),
            width=10,
            bg="#4CAF50",
            fg="white",
            command=self.register_user
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            buttons_frame,
            text="Login",
            font=("Arial", 12),
            width=10,
            bg="#2196F3",
            fg="white",
            command=self.login_user
        ).grid(row=0, column=1, padx=10)
        
        tk.Button(
            buttons_frame,
            text="Exit",
            font=("Arial", 12),
            width=10,
            bg="#f44336",
            fg="white",
            command=self.root.destroy
        ).grid(row=0, column=2, padx=10)
    
    def setup_todo_frame(self):
        # Header with welcome and logout
        self.header_frame = tk.Frame(self.todo_frame, bg="#f5f5f5")
        self.header_frame.pack(fill=tk.X, pady=10)
        
        self.welcome_label = tk.Label(
            self.header_frame, 
            text="Welcome!", 
            font=("Arial", 14, "bold"),
            bg="#f5f5f5"
        )
        self.welcome_label.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            self.header_frame,
            text="Analytics",
            font=("Arial", 10),
            bg="#9C27B0",
            fg="white",
            command=self.show_analytics
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            self.header_frame,
            text="Logout",
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            command=self.logout
        ).pack(side=tk.RIGHT, padx=5)
        
        # Todo entry
        entry_frame = tk.Frame(self.todo_frame, bg="#f5f5f5")
        entry_frame.pack(fill=tk.X, pady=10, padx=10)
        
        self.todo_entry = tk.Entry(entry_frame, font=("Arial", 12), width=40)
        self.todo_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            entry_frame,
            text="Add Task",
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            command=self.add_task
        ).pack(side=tk.RIGHT)
        
        # Todo list
        list_frame = tk.Frame(self.todo_frame, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.todo_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 12),
            height=10,
            width=40,
            selectbackground="#a6a6a6"
        )
        self.todo_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Connect scrollbar to listbox
        self.todo_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.todo_listbox.yview)
        
        # Feedback label
        self.todo_feedback = tk.Label(
            self.todo_frame, 
            text="", 
            font=("Arial", 10),
            bg="#f5f5f5",
            fg="red"
        )
        self.todo_feedback.pack()
        
        # Control buttons
        controls_frame = tk.Frame(self.todo_frame, bg="#f5f5f5")
        controls_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(
            controls_frame,
            text="Delete Task",
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            command=self.delete_task
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            controls_frame,
            text="Complete Task",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            command=self.complete_task
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            controls_frame,
            text="Edit Task",
            font=("Arial", 10),
            bg="#FF9800",
            fg="white",
            command=self.edit_task
        ).pack(side=tk.LEFT, padx=10)
    
    def setup_analytics_frame(self):
        # Header
        header_frame = tk.Frame(self.analytics_frame, bg="#f5f5f5")
        header_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            header_frame, 
            text="Productivity Analytics", 
            font=("Arial", 16, "bold"),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            header_frame,
            text="Back to Tasks",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            command=self.back_to_todo
        ).pack(side=tk.RIGHT, padx=10)
        
        # Frame for the chart
        self.chart_frame = tk.Frame(self.analytics_frame, bg="#f5f5f5")
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def register_user(self):
        name = self.name_entry.get().strip()
        password = self.password_entry.get()
        
        if not name:
            self.auth_feedback.config(text="Please enter a name.")
            return
        
        if len(password) < 8:
            self.auth_feedback.config(text="Password must be at least 8 characters long.")
            return
        
        if name in self.user_data:
            self.auth_feedback.config(text="User already exists. Please log in.")
            return
        
        self.user_data[name] = {
            "password": password,
            "todos": [],
            "activity": {}
        }
        
        self.save_user_data()
        self.auth_feedback.config(text="Registration successful! You can now login.", fg="green")
        self.password_entry.delete(0, tk.END)
    
    def login_user(self):
        name = self.name_entry.get().strip()
        password = self.password_entry.get()
        
        if not name or name not in self.user_data:
            self.auth_feedback.config(text="User not found. Please register first.")
            return
        
        if self.user_data[name]["password"] != password:
            self.auth_feedback.config(text="Incorrect password. Please try again.")
            return
        
        self.current_user = name
        self.welcome_label.config(text=f"Welcome, {name}!")
        
        # Initialize activity tracking if not present
        if "activity" not in self.user_data[self.current_user]:
            self.user_data[self.current_user]["activity"] = {}
        
        # Log login activity
        today = datetime.date.today().isoformat()
        if today not in self.user_data[self.current_user]["activity"]:
            self.user_data[self.current_user]["activity"][today] = {
                "completed": 0,
                "added": 0,
                "total": len(self.user_data[self.current_user]["todos"])
            }
        
        # Update the todo list
        self.update_todo_list()
        
        # Switch to todo frame
        self.auth_frame.pack_forget()
        self.todo_frame.pack(fill=tk.BOTH, expand=True)
        
        # Reset feedback labels
        self.auth_feedback.config(text="")
        self.todo_feedback.config(text="")
    
    def logout(self):
        self.current_user = None
        self.name_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.todo_frame.pack_forget()
        self.analytics_frame.pack_forget()
        self.auth_frame.pack(fill=tk.BOTH, expand=True)
        self.auth_feedback.config(text="")
    
    def update_todo_list(self):
        self.todo_listbox.delete(0, tk.END)
        
        if self.current_user and "todos" in self.user_data[self.current_user]:
            for todo in self.user_data[self.current_user]["todos"]:
                status = "✓ " if todo["completed"] else "  "
                self.todo_listbox.insert(tk.END, f"{status}{todo['text']}")
    
    def add_task(self):
        task = self.todo_entry.get().strip()
        
        if not task:
            self.todo_feedback.config(text="Task cannot be empty.")
            return
        
        today = datetime.date.today().isoformat()
        
        # Add task
        self.user_data[self.current_user]["todos"].append({
            "text": task,
            "completed": False,
            "date_added": today
        })
        
        # Update activity
        if today not in self.user_data[self.current_user]["activity"]:
            self.user_data[self.current_user]["activity"][today] = {
                "completed": 0,
                "added": 0,
                "total": len(self.user_data[self.current_user]["todos"])
            }
        
        self.user_data[self.current_user]["activity"][today]["added"] += 1
        self.user_data[self.current_user]["activity"][today]["total"] = len(self.user_data[self.current_user]["todos"])
        
        self.save_user_data()
        self.todo_entry.delete(0, tk.END)
        self.update_todo_list()
        self.todo_feedback.config(text="Task added successfully!", fg="green")
    
    def delete_task(self):
        try:
            index = self.todo_listbox.curselection()[0]
            del self.user_data[self.current_user]["todos"][index]
            
            # Update activity
            today = datetime.date.today().isoformat()
            if today in self.user_data[self.current_user]["activity"]:
                self.user_data[self.current_user]["activity"][today]["total"] = len(self.user_data[self.current_user]["todos"])
            
            self.save_user_data()
            self.update_todo_list()
            self.todo_feedback.config(text="Task deleted successfully!", fg="green")
        except:
            self.todo_feedback.config(text="Please select a task to delete.")
    
    def complete_task(self):
        try:
            index = self.todo_listbox.curselection()[0]
            task_completed = not self.user_data[self.current_user]["todos"][index]["completed"]
            self.user_data[self.current_user]["todos"][index]["completed"] = task_completed
            
            # Update activity for completion
            today = datetime.date.today().isoformat()
            if today not in self.user_data[self.current_user]["activity"]:
                self.user_data[self.current_user]["activity"][today] = {
                    "completed": 0,
                    "added": 0,
                    "total": len(self.user_data[self.current_user]["todos"])
                }
            
            if task_completed:
                self.user_data[self.current_user]["activity"][today]["completed"] += 1
            else:
                # If uncompleting a task
                self.user_data[self.current_user]["activity"][today]["completed"] = max(
                    0, self.user_data[self.current_user]["activity"][today]["completed"] - 1
                )
            
            self.save_user_data()
            self.update_todo_list()
            
            status = "completed" if task_completed else "marked incomplete"
            self.todo_feedback.config(text=f"Task {status}!", fg="green")
        except:
            self.todo_feedback.config(text="Please select a task to mark as complete.")
    
    def edit_task(self):
        try:
            index = self.todo_listbox.curselection()[0]
            current_task = self.user_data[self.current_user]["todos"][index]["text"]
            
            new_task = simpledialog.askstring("Edit Task", "Update task:", initialvalue=current_task)
            
            if new_task and new_task.strip():
                self.user_data[self.current_user]["todos"][index]["text"] = new_task.strip()
                self.save_user_data()
                self.update_todo_list()
                self.todo_feedback.config(text="Task updated successfully!", fg="green")
        except:
            self.todo_feedback.config(text="Please select a task to edit.")
    
    def show_analytics(self):
        self.todo_frame.pack_forget()
        self.analytics_frame.pack(fill=tk.BOTH, expand=True)
        
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        self.create_productivity_chart()
    
    def create_productivity_chart(self):
        # Prepare data for visualization
        activity_data = self.user_data[self.current_user]["activity"]
        
        if not activity_data:
            # Show a message if no data
            tk.Label(
                self.chart_frame,
                text="No activity data available yet.\nComplete some tasks to see your productivity!",
                font=("Arial", 12),
                bg="#f5f5f5",
                pady=20
            ).pack()
            return
        
        # Convert data to DataFrame for easier manipulation with seaborn
        dates = []
        completed_tasks = []
        added_tasks = []
        total_tasks = []
        
        # Get the last 14 days
        today = datetime.date.today()
        date_list = [(today - datetime.timedelta(days=i)).isoformat() for i in range(13, -1, -1)]
        
        for date in date_list:
            if date in activity_data:
                dates.append(date)
                completed_tasks.append(activity_data[date]["completed"])
                added_tasks.append(activity_data[date]["added"])
                total_tasks.append(activity_data[date]["total"])
            else:
                # Add zeros for missing dates to maintain timeline
                dates.append(date)
                completed_tasks.append(0)
                added_tasks.append(0)
                # Use previous total or 0 if it's the first entry
                if total_tasks:
                    total_tasks.append(total_tasks[-1])
                else:
                    total_tasks.append(0)
        
        # Convert to pandas DataFrame
        df = pd.DataFrame({
            'Date': dates,
            'Completed': completed_tasks,
            'Added': added_tasks,
            'Total': total_tasks
        })
        
        # Format dates to be more readable
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%m/%d')
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [1, 1]})
        fig.subplots_adjust(hspace=0.3)
        
        # Plot 1: Daily Completed vs Added Tasks
        sns.set_style("whitegrid")
        bar_width = 0.35
        x = np.arange(len(df['Date']))
        
        ax1.bar(x - bar_width/2, df['Completed'], bar_width, label='Completed', color='#2196F3')
        ax1.bar(x + bar_width/2, df['Added'], bar_width, label='Added', color='#4CAF50')
        
        ax1.set_title('Daily Task Activity')
        ax1.set_xlabel('')
        ax1.set_ylabel('Number of Tasks')
        ax1.set_xticks(x)
        ax1.set_xticklabels(df['Date'], rotation=45)
        ax1.legend()
        
        # Plot 2: Total Tasks Trend
        sns.lineplot(x='Date', y='Total', data=df, marker='o', ax=ax2, color='#9C27B0')
        ax2.set_title('Total Tasks Over Time')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Total Tasks')
        ax2.set_xticks(range(len(df['Date'])))
        ax2.set_xticklabels(df['Date'], rotation=45)
        
        # Add the plot to the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def back_to_todo(self):
        self.analytics_frame.pack_forget()
        self.todo_frame.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = NimbusTodoApp(root)
    root.mainloop()