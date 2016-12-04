"""
logika tworzenia GUT zapakowana w metodzie wywolywanej z konstruktora aplikacji
"""
import tkinter as tk


class MyApp():
    def __init__(self, root):
        self.root = root
        self.createWidgets()

    def createWidgets(self):
        myContainer1 = tk.Frame(self.root)
        myContainer1.pack()

        button1 = tk.Button(myContainer1)
        button1.config(text="Hello, World!")
        button1.config(background="green")
        button1.pack()


root = tk.Tk()

myApp = MyApp(root)

root.mainloop()
