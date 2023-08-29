import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime
import requests
from tkcalendar import Calendar
import pyttsx3
import json

class Task:
    def __init__(self, description, due_date):
        self.description = description
        self.due_date = due_date

    def __str__(self):
        return f"{self.description} due {self.due_date}"

class Notification:
    def __init__(self, title, message, notify_time):
        self.title = title
        self.message = message
        self.notify_time = notify_time

    def __str__(self):
        return f"{self.title}: {self.message} at {self.notify_time}"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.notifications = []

    def add_task(self, task):
        self.tasks.append(task)

    def add_notification(self, notification):
        self.notifications.append(notification)

    def delete_task(self, index):
        self.tasks.pop(index)

    def delete_notification(self, index):
        self.notifications.pop(index)

    def get_suggestions(self, text):
        api_key = "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"
        prompt = text
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "prompt": prompt,
            "max_tokens": 100
        }

        response = requests.post(
            "https://api.openai.com/v1/engines/davinci-codex/completions",
            json=data,
            headers=headers
        )

        response_data = response.json()
        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["text"]
        else:
            return "No suggestions available."


class GUI:
    def __init__(self, task_manager):
        self.task_manager = task_manager

        self.window = tk.Tk()
        self.window.title("Task Manager")

        style = ttk.Style()
        style.theme_use('alt')

        self.task_frame = tk.Frame(master=self.window)
        self.task_frame.grid(row=0, column=0)

        self.notification_frame = tk.Frame(master=self.window)
        self.notification_frame.grid(row=0, column=1)

        self.task_list = tk.Listbox(self.task_frame)
        self.refresh_task_list()
        self.task_list.grid(row=0, column=0)

        self.notification_list = tk.Listbox(self.notification_frame)
        self.refresh_notification_list()
        self.notification_list.grid(row=0, column=0)

        self.task_input = tk.Entry(self.task_frame)
        self.task_input.grid(row=1, column=0)

        self.date_label = tk.Label(self.task_frame, text="Due Date")
        self.date_label.grid(row=2, column=0)

        self.calendar = Calendar(self.task_frame, selectmode='day', year=2023)
        self.calendar.grid(row=3, column=0)

        self.time_label = tk.Label(self.task_frame, text="Due Time (HH:MM)")
        self.time_label.grid(row=4, column=0)

        self.time_input = tk.Entry(self.task_frame)
        self.time_input.grid(row=5, column=0)

        self.add_task_btn = tk.Button(self.task_frame, text="Add Task", command=self.add_task)
        self.add_task_btn.grid(row=6, column=0)

        self.edit_task_btn = tk.Button(self.task_frame, text="Edit Task", command=self.edit_task)
        self.edit_task_btn.grid(row=7, column=0)

        self.delete_task_btn = tk.Button(self.task_frame, text="Delete Task", command=self.delete_task)
        self.delete_task_btn.grid(row=8, column=0)

        self.notification_title = tk.Entry(self.notification_frame)
        self.notification_title.grid(row=1, column=0)

        self.notification_message = tk.Entry(self.notification_frame)
        self.notification_message.grid(row=2, column=0)

        self.notification_time = tk.Entry(self.notification_frame)
        self.notification_time.grid(row=3, column=0)

        self.add_notification_btn = tk.Button(self.notification_frame, text="Add Notification",
                                              command=self.add_notification)
        self.add_notification_btn.grid(row=4, column=0)

        self.edit_notification_btn = tk.Button(self.notification_frame, text="Edit Notification",
                                               command=self.edit_notification)
        self.edit_notification_btn.grid(row=5, column=0)

        self.delete_notification_btn = tk.Button(self.notification_frame, text="Delete Notification",
                                                 command=self.delete_notification)
        self.delete_notification_btn.grid(row=6, column=0)

        self.suggestion_label = tk.Label(self.window, text="Suggestions")
        self.suggestion_label.grid(row=1, column=0)

        self.suggestion_text = tk.Text(self.window, height=10, width=50)
        self.suggestion_text.grid(row=2, column=0, columnspan=2)

        self.load_data()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_data()
        self.window.mainloop()


    def refresh_task_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_list.insert(tk.END, str(task))

    def refresh_notification_list(self):
        self.notification_list.delete(0, tk.END)
        for notification in self.task_manager.notifications:
            self.notification_list.insert(tk.END, str(notification))

    def show_notification(self, notification):
        engine = pyttsx3.init()
        engine.say(notification.message)
        engine.runAndWait()

        notify_window = tk.Toplevel()
        notify_window.title(notification.title)
        label = tk.Label(notify_window, text=notification.message)
        label.pack()

    def add_task(self):
        description = self.task_input.get()
        due_date = self.calendar.get_date()
        due_time = self.time_input.get()

        if not description or not due_date:
            messagebox.showerror("Error", "Please fill in all the fields")
            return

        try:
            due_date = datetime.strptime(due_date, "%m/%d/%y").date()  # Convert to date object
            if due_time:
                due_time = datetime.strptime(due_time, "%H:%M").time()  # Convert to time object
                due_datetime = datetime.combine(due_date, due_time)
            else:
                due_datetime = due_date
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format")
            return

        task = Task(description, due_datetime)
        self.task_manager.add_task(task)
        self.refresh_task_list()

    def edit_task(self):
        try:
            index = self.task_list.curselection()[0]
            task = self.task_manager.tasks[index]
        except IndexError:
            messagebox.showerror("Error", "No task selected")
            return

        new_description = simpledialog.askstring("Edit Task", "Enter new description:", initialvalue=task.description)
        if new_description is None:
            return

        new_due_date = simpledialog.askstring("Edit Task", "Enter new due date (yyyy-mm-dd):",
                                              initialvalue=task.due_date.strftime("%Y-%m-%d"))
        if new_due_date is None:
            return

        new_due_time = simpledialog.askstring("Edit Task", "Enter new due time (HH:MM):",
                                              initialvalue=task.due_date.strftime("%H:%M"))
        if new_due_time is None:
            return

        new_due_datetime = datetime.strptime(new_due_date, "%Y-%m-%d").date()
        new_due_datetime = new_due_datetime.replace(hour=int(new_due_time[:2]), minute=int(new_due_time[3:]))

        task.description = new_description
        task.due_date = new_due_datetime

        self.refresh_task_list()

    def delete_task(self):
        try:
            index = self.task_list.curselection()[0]
            self.task_manager.delete_task(index)
            self.refresh_task_list()
        except IndexError:
            messagebox.showerror("Error", "No task selected")
            return

    def add_notification(self):
        title = self.notification_title.get()
        message = self.notification_message.get()
        notify_time = self.notification_time.get()

        notification = Notification(title, message, notify_time)
        self.task_manager.add_notification(notification)
        self.refresh_notification_list()

        self.notification_title.delete(0, tk.END)
        self.notification_message.delete(0, tk.END)
        self.notification_time.delete(0, tk.END)

    def edit_notification(self):
        try:
            index = self.notification_list.curselection()[0]
            notification = self.task_manager.notifications[index]
        except IndexError:
            messagebox.showerror("Error", "No notification selected")
            return

        new_title = simpledialog.askstring("Edit Notification", "Enter new title:", initialvalue=notification.title)
        if new_title is None:
            return

        new_message = simpledialog.askstring("Edit Notification", "Enter new message:",
                                             initialvalue=notification.message)
        if new_message is None:
            return

        new_notify_time = simpledialog.askstring("Edit Notification", "Enter new notification time (HH:MM):",
                                                 initialvalue=notification.notify_time)
        if new_notify_time is None:
            return

        notification.title = new_title
        notification.message = new_message
        notification.notify_time = new_notify_time

        self.refresh_notification_list()

    def delete_notification(self):
        try:
            index = self.notification_list.curselection()[0]
            self.task_manager.delete_notification(index)
            self.refresh_notification_list()
        except IndexError:
            messagebox.showerror("Error", "No notification selected")
            return

    def save_data(self):
        data = {
            "tasks": [
                {"description": task.description, "due_date": task.due_date.strftime("%m/%d/%y %H:%M")}
                for task in self.task_manager.tasks
            ],
            "notifications": [
                {"title": notification.title, "message": notification.message, "notify_time": notification.notify_time}
                for notification in self.task_manager.notifications
            ]
        }
        with open("data.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                for task_data in data["tasks"]:
                    due_date = datetime.strptime(task_data["due_date"], "%m/%d/%y %H:%M")
                    task = Task(task_data["description"], due_date)
                    self.task_manager.add_task(task)
                for notification_data in data["notifications"]:
                    notification = Notification(
                        notification_data["title"],
                        notification_data["message"],
                        notification_data["notify_time"]
                    )
                    self.task_manager.add_notification(notification)
                self.refresh_task_list()
                self.refresh_notification_list()
        except FileNotFoundError:
            pass

    def on_closing(self):
        self.save_data()
        self.window.destroy()

if __name__ == "__main__":
    task_manager = TaskManager()
    gui = GUI(task_manager)
    gui.window.mainloop()
