"""
dowiązywanie wielu handlerów do jednego zdarzenia
"""
import tkinter as tk


class MyApp:
    def __init__(self, root):
        self.root = root
        button = tk.Button(text="OK", command=self.say_hello)  # event handler
        button.pack()
        button.focus_force()
        button.bind("<Button-1>", self.event_handler_first)
        button.bind("<Button-1>", self.event_handler_second, "+")

    # button.bind("<Button-1>" , self.event_handler_second)

    def say_hello(self):
        print("Hi!")

    def event_handler_first(self, event):
        print("first_handler")

    def event_handler_second(self, event):
        print("second_handler")


root = tk.Tk()
myapp = MyApp(root)
root.mainloop()
