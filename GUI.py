import tkinter as tk
from tkinter import ttk
from Main File.py
from tkinter.messagebox import showinfo

class App(tk.Tk):
  def __init__(self):
    super().__init__()

    # configure the root window
    self.title('Budget Tracker')
    self.geometry('900x700')
    self.label = tk.Label(self, text='Budget Tracker')
    self.label.pack()
    self.setup()


    # self.button = tk.Button(self, text='Click Me')
    # self.button['command'] = self.button_clicked
    # self.button.pack()

  def setup(self): # This will need to return an update
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    self.combo_box = ttk.Combobox(self, values=months)
    self.combo_box.set("Select a month")
    self.combo_box.pack()

  def percent_bar(self):



if __name__ == "__main__":
  app = App()
  app.mainloop()

