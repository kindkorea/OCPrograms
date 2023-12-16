
import tkinter as tk
from tkinter import ttk
from tkinter import * # __all__
import math
import gui_pdf2jpg
import gui_faxReceive
import gui_calculator

import gui_fax_pdf

class ControlFrame(Frame):
    def __init__(self, container):
        super().__init__(container)
   
        f = Frame(self)
        
        self.menu_list = {
            0 : ['컨버터 및 팩스'],
            1 : ['마진 계산기']
        }
        self.NUMBER_TITLE = 0
        self.NUMBER_FRAME = 1
        
        for ix , key in enumerate(self.menu_list.keys()):
            e = Button(f , text=self.menu_list[key][self.NUMBER_TITLE],command=lambda x=key: [self.change_frame(x)])
            e.grid(row=0, column=ix)
            
            # Button(f , text='app2',command=lambda x=1 : self.change_frame(x)).grid(row=0, column=1)
            
        f.grid(row=0, column=0 , sticky='w' , pady=20)
        
        self.grid(column=0, row=0, padx=5, pady=5, sticky='ew')
        
        self.frames = {}

        self.menu_list[0].append(gui_fax_pdf.FaxPdf(container))
        self.menu_list[1].append(gui_calculator.Calculator(container))
        
        self.current_frame = self.menu_list[0][self.NUMBER_FRAME]
        self.change_frame(0)
        
        
    def change_frame(self,x):
        print(x)
        self.current_frame.grid_forget()
        self.current_frame = self.menu_list[x][self.NUMBER_FRAME]
        self.current_frame.grid(row =1, column=0)
        
        
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('웅천목재 프로그램')
        self.geometry('600x800')


if __name__ == "__main__":
    app = App()
    ControlFrame(app)
    app.mainloop()
    
    