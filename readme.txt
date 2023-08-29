   Task Manager with Notifications
This is a simple task manager application that allows you to manage tasks and set notifications for them. The application is built using the Tkinter library for the graphical user interface and includes features such as adding, editing, and deleting tasks, as well as adding, editing, and deleting notifications.
   Features
* Add tasks with descriptions, due dates, and optional due times.
* Edit existing tasks to update their descriptions, due dates, and due times.
* Delete tasks that are no longer needed.
* Add notifications with titles, messages, and notification times.
* Edit existing notifications to update their titles, messages, and notification times.
* Delete notifications that are no longer needed.
* Receive notifications with text-to-speech capabilities.
   Prerequisites
Before running the application, make sure you have the following:
* Python installed on your system.
* The required libraries installed. You can install them using pip:
 pip install tk tkcalendar pyttsx3 requests
  How to Use
* Run the program by executing the main.py file using Python:
python main.py
* The application's main window will open. The left side of the window is dedicated to managing tasks, while the right side is for managing notifications.
* To add a task, enter the task description, select the due date from the calendar, and optionally enter the due time. Then click the "Add Task" button.
* To edit a task, select the task from the task list, click the "Edit Task" button, and follow the prompts to make changes.
* To delete a task, select the task from the task list and click the "Delete Task" button.
* To add a notification, enter the notification title, message, and notification time. Then click the "Add Notification" button.
* To edit a notification, select the notification from the notification list, click the "Edit Notification" button, and follow the prompts to make changes.
* To delete a notification, select the notification from the notification list and click the "Delete Notification" button.
* The "Suggestions" section in the application provides AI-powered text suggestions based on your input. It uses the OpenAI Codex API for suggestions.
  Data Persistence
The application saves tasks and notifications to a JSON file named data.json in the same directory. Data is loaded from this file when the application starts and is saved when the application is closed.
  Notifications
The application schedules notifications using the schedule library. Notifications are displayed as message boxes and read aloud using the pyttsx3 library's text-to-speech capabilities.
  Credits
This application was developed using the Tkinter library for the GUI, the OpenAI Codex API for text suggestions, and various other Python libraries for handling notifications and data.