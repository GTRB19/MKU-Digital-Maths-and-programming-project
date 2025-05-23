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

# import tkinter as tk
#
# class NewWindow(tk.Toplevel):
#     """Represents a new independent window."""
#     def __init__(self, parent=None, main_window=None, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         self.main_window = main_window  # Store a reference to the main window
#         self.title("New Window")
#         self.geometry("300x200")
#         self.label = tk.Label(self, text="This is a new window!")
#         self.label.pack(padx=20, pady=20)
#         self.focus_set()
#         self.grab_set()
#         self.protocol("WM_DELETE_WINDOW", self.close_new_window) # Handle window close button
#
#     def close_new_window(self):
#         """Closes the new window and optionally the main window."""
#         if self.main_window:
#             self.main_window.destroy()  # Destroy the main window
#         self.destroy()  # Destroy the new window
#
# class MainWindow(tk.Tk):
#     """The main application window."""
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.title("Main Application")
#         self.geometry("400x300")
#         self.open_button = tk.Button(self, text="Open New Window", command=self.open_new_window)
#         self.open_button.pack(pady=20)
#
#     def open_new_window(self):
#         """Creates and displays the NewWindow and closes the MainWindow."""
#         new_window = NewWindow(self, main_window=self) # Pass a reference to self
#         # self.withdraw()  # Hide the main window (optional, but often desired)
#         # self.center_window(new_window)
#
#     def center_window(self, window):
#         """Centers the given window relative to the screen."""
#         window.update_idletasks()
#         screen_width = self.winfo_screenwidth()
#         screen_height = self.winfo_screenheight()
#         child_width = window.winfo_width()
#         child_height = window.winfo_height()
#         x = (screen_width - child_width) // 2
#         y = (screen_height - child_height) // 2
#         window.geometry(f"+{x}+{y}")
#
# if __name__ == "__main__":
#     app = MainWindow()
#     app.mainloop()


import tkinter as tk
import pandas as pd
from pandastable import Table, TableModel

class PandasTableApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PandasTable Update Checker")

        # Create a sample DataFrame
        self.df = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [30, 24, 35],
            'City': ['New York', 'London', 'Paris']
        })

        # Create a frame to hold the table
        self.table_frame = tk.Frame(master)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create the pandastable widget
        self.table = pt = Table(self.table_frame, dataframe=self.df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()

        # Store an original snapshot of the DataFrame
        # IMPORTANT: Use .copy(deep=True) to create a completely independent copy.
        # Otherwise, changes to self.df will also affect self.original_df_snapshot.
        self.original_df_snapshot = self.df.copy(deep=True)

        # Add a button to check for updates
        self.check_button = tk.Button(master, text="Check for Updates", command=self.check_for_updates)
        self.check_button.pack(pady=5)

        # Add a button to "save" changes (update the snapshot)
        self.save_button = tk.Button(master, text="Save Changes", command=self.save_changes)
        self.save_button.pack(pady=5)

        self.status_label = tk.Label(master, text="No updates yet.")
        self.status_label.pack(pady=5)

    def check_for_updates(self):
        # Access the current DataFrame from the table's model
        current_df = self.table.model.df

        # Compare the current DataFrame with the original snapshot
        if not current_df.equals(self.original_df_snapshot):
            self.status_label.config(text="Table values have been updated!", fg="red")

            # Optional: Print the differences
            print("Original Data:")
            print(self.original_df_snapshot)
            print("\nCurrent Data:")
            print(current_df)

            # Highlight specific changes (this can be complex for large DFs)
            diff_df = current_df.compare(self.original_df_snapshot)
            if not diff_df.empty:
                print("\nDifferences:")
                print(diff_df)
        else:
            self.status_label.config(text="No updates detected.", fg="black")

    def save_changes(self):
        # Access the current DataFrame
        current_df = self.table.model.df

        # Update the original snapshot to the current state
        self.original_df_snapshot = current_df.copy(deep=True)
        self.status_label.config(text="Changes saved (snapshot updated).", fg="green")
        print("DataFrame snapshot updated to current values.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PandasTableApp(root)
    root.mainloop()