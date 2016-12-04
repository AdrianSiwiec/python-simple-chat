"""
Przekazywanie danych do event_handler'a - inna metoda.
"""
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.createWidgets()

    def createWidgets(self):
        self.sapper_buttons = []
        L1 = list(range(8))
        L2 = list(range(8))
        for i in range(8):
            self.sapper_buttons.append([])
            for j in range(8):
                def handler(i=i, j=j):
                    self.sapperButtonPressed(i, j)

                self.sapper_buttons[i].append(tk.Button(self, text="(" + str(i) + "," + str(j) + ")", command=handler))
                self.sapper_buttons[i][j].grid(row=i, column=j, sticky=tk.N + tk.S + tk.E + tk.W)

        for i in range(8):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        self.newGameButton = tk.Button(self, text='New game', command=self.newGame)
        self.newGameButton.grid(row=8, column=0, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=8, column=4, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)

        self.rowconfigure(8, weight=2)

    def sapperButtonPressed(self, i, j):
        print("SapperButtonPressed: i = ", i, " j=", j)

    def newGame(self):
        print("New Game")


app = Application()
app.master.title('Sapper')
app.mainloop()
