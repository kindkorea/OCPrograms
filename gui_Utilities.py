import gui_pdf2jpg
import gui_faxReceive
import tkinter as tk

class Utilities():
    def __init__(self, containerFrame):
        self.container = containerFrame
        
        self.a = tk.Frame(self.container)
        gui_pdf2jpg.Pdf2jpg(self.a)
        self.a.grid(row=1 , column=0 )
        
        self.b = tk.Frame(self.container)
        gui_faxReceive.GUI_FaxReceive(self.b)
        self.b.grid(row=2 , column=0 , pady = 20)