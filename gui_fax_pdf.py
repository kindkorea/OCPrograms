import gui_pdf2jpg
import gui_faxReceive
import tkinter as tk
from tkinter import ttk
from tkinter import * # __all__




class FaxPdf(Frame):
    def __init__(self, container):
        super().__init__(container)
    
        a = gui_pdf2jpg.Pdf2jpg(self)
        a.grid(row=1 , column=0 )
        
        b = gui_faxReceive.GUI_FaxReceive(self)
        b.grid(row=2 , column=0 , pady = 20)
        
        
 