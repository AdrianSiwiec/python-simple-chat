"""
demonstracja ukladacza grid
"""
import tkinter as tk

class MyApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Moja aplikacja")
		self.root.minsize(600,400)
		self.mainFrame = tk.Frame(self.root)
		self.mainFrame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
		self.root.rowconfigure(0, weight=1)
		self.root.columnconfigure(0, weight=1)
		
		self.frame00 = tk.Frame(self.mainFrame, bg="green")
		self.frame00.grid(column=0, row=0, sticky=tk.N + tk.S + tk.W + tk.E)

		self.frame01 = tk.Frame(self.mainFrame, bg="blue")
		self.frame01.grid(column=1, row=0, rowspan=2, sticky=tk.N + tk.S + tk.W + tk.E)

		self.frame10 = tk.Frame(self.mainFrame, bg="red")
		self.frame10.grid(column=0, row=1, sticky=tk.N + tk.S + tk.W + tk.E)

		self.frame20 = tk.Frame(self.mainFrame, bg="yellow")
		self.frame20.grid(column=0, row=2, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
		
		self.mainFrame.rowconfigure(0,weight=4)
		self.mainFrame.rowconfigure(1,weight=2)
		self.mainFrame.rowconfigure(2,weight=1)
		
		self.mainFrame.columnconfigure(0,weight=3)
		self.mainFrame.columnconfigure(1,weight=1)
		
		
root = tk.Tk()
myapp = MyApp(root)
root.mainloop()
