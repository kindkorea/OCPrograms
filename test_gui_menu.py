
import tkinter as tk
from tkinter import ttk
from tkinter import * # __all__
import math
import gui_pdf2jpg
import gui_faxReceive
import gui_calculator

class app1(ttk.Frame):
    def __init__(self, container,text):
        super().__init__(container)

        self.btn = Button(self, text=text ,command=self.btn_change)
        self.btn.grid(row=1, column=0)
        
        self.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
        
    def btn_change(self):
        self.btn.configure(bg='red')
        
class app2(ttk.Frame):
    def __init__(self, container,text):
        super().__init__(container)

        Button(self, text=text).grid(row=1, column=1)        
        self.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
    


class ControlFrame(Frame):
    def __init__(self, container):
        super().__init__(container)
   
        f = Frame(self)
        
        Button(f , text='app1',command=lambda x=0 : self.change_frame(x)).grid(row=0, column=0)
        Button(f , text='app2',command=lambda x=1 : self.change_frame(x)).grid(row=0, column=1)
        
        f.grid(row=0, column=0 , sticky='w')
        
        self.grid(column=0, row=0, padx=5, pady=5, sticky='ew')
        
        # f1 = Frame(self)
        # f1.grid(row=1,column=0)
        
        
        # # gui_faxReceive.GUI_FaxReceive(f1, 1, 0 )
        
        f2 = Frame(container)
        # f2.grid(row=1,column=0)
        
        
        
        
        self.frames = {}
        
        # self.frames.append(f2)
        # self.frames.append(f3)
        self.frames[0] = gui_pdf2jpg.Pdf2jpg(container, 1, 0, 8)
        self.frames[1] = gui_calculator.Calculator(container, 1, 0)
        
        
        self.current_frame = self.frames[0]
        
        self.change_frame(1)
        
        
    def change_frame(self,x):
        # self.grid_forget()
        self.current_frame.grid_forget()
        
        self.current_frame = self.frames[x]
        self.current_frame.grid(row =1, column=0)
        # # frame.reset()
        # print(frame)
        # frame.tkraise()
        
        
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Temperature Converter')
        self.geometry('600x800')
        # self.resizable(False, False)


if __name__ == "__main__":
    app = App()
    ControlFrame(app)
    app.mainloop()
    
    