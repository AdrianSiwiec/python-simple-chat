"""
Demonstracja różnych poziomów bindowania event handlerów:
- poziom instancji
- poziom klasy
- poziom aplikacji

Dla każdego widgetu, dla każdego poziomu bindowania, dla każdego zdarzenia, wywoływany jest handler, który
najbardziej odpowiada wygenerowanemu zdarzeniu. Np. po nacisnieciu ENTER, <Any-KeyPress> 
jest zasłaniane zdarzeniem <RETURN>.

Ponadto, demonstracja użycia funkcji anonimowych jako handlerów.
"""
import tkinter as tk


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Moja aplikacja")
        self.root.minsize(600, 400)
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.mainFrame.myName = "MainFrame"
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.frame00 = tk.Frame(self.mainFrame, bg="green")
        self.frame00.grid(column=0, row=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.frame00.myName = "Frame00"

        self.frame01 = tk.Frame(self.mainFrame, bg="blue")
        self.frame01.grid(column=1, row=0, rowspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
        self.frame01.myName = "Frame01"

        self.frame10 = tk.Frame(self.mainFrame, bg="red")
        self.frame10.grid(column=0, row=1, sticky=tk.N + tk.S + tk.W + tk.E)
        self.frame10.myName = "Frame10"

        self.frame20 = tk.Frame(self.mainFrame, bg="yellow")
        self.frame20.grid(column=0, row=2, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
        self.frame20.myName = "Frame20"

        self.mainFrame.rowconfigure(0, weight=4)
        self.mainFrame.rowconfigure(1, weight=2)
        self.mainFrame.rowconfigure(2, weight=1)

        self.mainFrame.columnconfigure(0, weight=3)
        self.mainFrame.columnconfigure(1, weight=1)

        self.ok_button = tk.Button(self.frame20, text="OK")
        self.ok_button.pack()
        self.ok_button.myName = "OK Button"
        self.ok_button.focus_force()

        self.no_button = tk.Button(self.frame20, text="NO")
        self.no_button.myName = "No Button"
        self.no_button.pack()

        # bindowanie na poziomie instancji
        self.ok_button.bind('<Any-KeyPress>',
                            lambda event: self.handler(event, level="Object", event_name="<Any-KeyPress>"))
        self.ok_button.bind('<Return>', lambda event: self.handler(event, level="Object", event_name="<Return>"))
        self.no_button.bind('<Any-KeyPress>',
                            lambda event: self.handler(event, level="Object", event_name="<Any-KeyPress>"))
        self.no_button.bind('<Return>', lambda event: self.handler(event, level="Object", event_name="<Return>"))

        # bindowanie na poziomie klasy (do wszystkich elementow klasy)
        self.root.bind_class('Frame', '<Configure>',
                             lambda event: self.handler(event, level='Class', event_name='<Configure>'))
        self.root.bind_class('Button', '<Return>',
                             lambda event: self.handler(event, level='Class', event_name="<Return>"))

        # bindowanie na poziomie aplikacji
        self.root.bind_all("<Return>", lambda event: self.handler(event, level='Application', event_name='<Return>'))
        self.root.bind_all("<Any-KeyPress>",
                           lambda event: self.handler(event, level='Application', event_name='<Any-KeyPress>'))

    def handler(self, event, level, event_name):
        print("Widget:", event.widget.myName, " launched event ", event_name, " at level:", level)


root = tk.Tk()
myapp = MyApp(root)
root.mainloop()
