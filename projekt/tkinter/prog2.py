import tkinter as tk

root = tk.Tk()  # tworzy okno główne aplikacji pod standardową nazwą root

"""
utworzenie obiektu Frame (kontener na inne widgety) 
i ustawienie zaleznosci logicznej: widget mainFrame zawarty w root (ktory sam jest kontenerem)
"""
mainFrame = tk.Frame(root)
mainFrame.pack() #ustawienie polozenia obiektu w kontenerze

button1 = tk.Button(mainFrame) # utworzenie widgetu Button, ustawienie logicznej zaleznosci: button nalezy do kontenera mainFrame
button1["text"] = "Hello, World!" 
button1["background"] = "green"

button1.pack() # okreslenie polozenia obiektu button w kontenerze

root.mainloop() # odpalenie petli glownej GUI 

