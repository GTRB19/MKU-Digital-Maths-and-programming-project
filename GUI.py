# import tkinter as tk
# from tkinter import ttk
# from Main file.py import return monthly dashboard
# from tkinter.messagebox import showinfo

# class App(tk.Tk):
#   def __init__(self):
#     super().__init__()
#
#     # configure the root window
#     self.title('Budget Tracker')
#     self.geometry('900x700')
#     self.label = tk.Label(self, text='Budget Tracker')
#     self.label.pack()
#     self.setup()
#
#
#     # self.button = tk.Button(self, text='Click Me')
#     # self.button['command'] = self.button_clicked
#     # self.button.pack()
#
#   def setup(self): # This will need to return an update
#     months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
#     self.combo_box = ttk.Combobox(self, values=months)
#     self.combo_box.set("Select a month")
#     self.combo_box.pack()
#
#   def percent_bar(self):
#     Main
#
#
#
# if __name__ == "__main__":
#   app = App()
#   app.mainloop()


# import tkinter as tk
# from tkinter import ttk
#
# class windows(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#         # Adding a title to the window
#         self.wm_title("Test Application")
#
#         # creating a frame and assigning it to container
#         container = tk.Frame(self, height=400, width=600)
#         # specifying the region where the frame is packed in root
#         container.pack(side="top", fill="both", expand=True)
#
#         # configuring the location of the container using grid
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
#
#         # We will now create a dictionary of frames
#         self.frames = {}
#         # we'll create the frames themselves later but let's add the components to the dictionary.
#         for F in (MainPage, SidePage, CompletionScreen):
#             frame = F(container, self)
#
#             # the windows class acts as the root window for the frames.
#             self.frames[F] = frame
#             frame.grid(row=0, column=0, sticky="nsew")
#
#         # Using a method to switch frames
#         self.show_frame(MainPage)
#
#     def show_frame(self, cont):
#         frame = self.frames[cont]
#         # raises the current frame to the top
#         frame.tkraise()
#
#
# class MainPage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Main Page")
#         label.pack(padx=10, pady=10)
#
#         # We use the switch_window_button in order to call the show_frame() method as a lambda function
#         switch_window_button = tk.Button(
#             self,
#             text="Go to the Side Page",
#             command=lambda: controller.show_frame(SidePage),
#         )
#         switch_window_button.pack(side="bottom", fill=tk.X)
#
#
# class SidePage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="This is the Side Page")
#         label.pack(padx=10, pady=10)
#
#         switch_window_button = tk.Button(
#             self,
#             text="Go to the Completion Screen",
#             command=lambda: controller.show_frame(CompletionScreen),
#         )
#         switch_window_button.pack(side="bottom", fill=tk.X)
#
#
# class CompletionScreen(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Completion Screen, we did it!")
#         label.pack(padx=10, pady=10)
#         switch_window_button = ttk.Button(
#             self, text="Return to menu", command=lambda: controller.show_frame(MainPage)
#         )
#         switch_window_button.pack(side="bottom", fill=tk.X)
#
# if __name__ == "__main__":
#     testObj = windows()
#     testObj.mainloop()

import tkinter as tk

class NewWindow(tk.Toplevel):
    """Represents a new independent window."""
    def __init__(self, parent=None, main_window=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.main_window = main_window  # Store a reference to the main window
        self.title("New Window")
        self.geometry("300x200")
        self.label = tk.Label(self, text="This is a new window!")
        self.label.pack(padx=20, pady=20)
        self.focus_set()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.close_new_window) # Handle window close button

    def close_new_window(self):
        """Closes the new window and optionally the main window."""
        if self.main_window:
            self.main_window.destroy()  # Destroy the main window
        self.destroy()  # Destroy the new window

class MainWindow(tk.Tk):
    """The main application window."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Main Application")
        self.geometry("400x300")
        self.open_button = tk.Button(self, text="Open New Window", command=self.open_new_window)
        self.open_button.pack(pady=20)

    def open_new_window(self):
        """Creates and displays the NewWindow and closes the MainWindow."""
        new_window = NewWindow(self, main_window=self) # Pass a reference to self
        # self.withdraw()  # Hide the main window (optional, but often desired)
        # self.center_window(new_window)

    def center_window(self, window):
        """Centers the given window relative to the screen."""
        window.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        child_width = window.winfo_width()
        child_height = window.winfo_height()
        x = (screen_width - child_width) // 2
        y = (screen_height - child_height) // 2
        window.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()