import tkinter as tk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.mainFrame = tk.Frame(root)
        self.mainFrame.pack()

        self.button1 = tk.Button(self.mainFrame)
        self.button1.myName = "OK Button"
        self.button1.config(text="OK", background= "green")
        self.button1.pack(side=tk.LEFT)
        self.button1.focus_force() 
        self.button1.bind("<Button-1>", self.button1Click)
        self.button1.bind("<Return>", self.button1Click)

        self.button2 = tk.Button(self.mainFrame)
        self.button2.myName ="Cancel Button"
        self.button2.configure(text="Cancel", background="red")
        self.button2.pack(side=tk.RIGHT)
        self.button2.bind("<Button-1>", self.button2Click)
        self.button2.bind("<Return>", self.button2Click)

    def button1Click(self, event):
        report_event(event)
        if self.button1["background"] == "green":
            self.button1["background"] = "yellow"
        else:
            self.button1["background"] = "green"

    def button2Click(self, event):
        report_event(event)
        self.root.destroy()

def report_event(event):
    """
		Print a description of an event, based on its attributes.
    """
    event_name = {"2": "KeyPress", "4": "ButtonPress"}
    print("Time:", str(event.time))   ### (6)
    print("EventType=" + str(event.type), event_name[str(event.type)])
    print("Launched by widget:=" + event.widget.myName)


root = tk.Tk()
myapp = MyApp(root)
root.mainloop()
