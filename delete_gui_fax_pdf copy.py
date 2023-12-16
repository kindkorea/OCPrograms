import gui_pdf2jpg
import gui_faxReceive
import tkinter as tk
from tkinter import ttk
from tkinter import * # __all__



class FaxPdf(Frame):
    def __init__(self, container):
        super().__init__(container)
        
        # f = Frame(container)
        app = gui_pdf2jpg.Pdf2jpg(container)
        app.grid(row=0,column=0)
        app2 = gui_faxReceive.GUI_FaxReceive(container)
        app2.grid(row=1,column=0)
        
        # f.grid(row=0,column=0)
        
        

        
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('웅천목재 프로그램')
        self.geometry('600x800')


if __name__ == "__main__":
    app = App()
    app = FaxPdf(app)
    app.grid(row=0, column=0)
    app.mainloop()
    
    
 
 