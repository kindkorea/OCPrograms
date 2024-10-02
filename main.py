
import tkinter as tk
from tkinter import ttk
from tkinter import * # __all__
import PIL
import math
import gui_pdf2jpg
import gui_faxReceive
import gui_calculator
import gui_pdf2jpg
import win32clipboard


class FaxPdf(Frame):
    def __init__(self, container):
        super().__init__(container)
    
        a = gui_pdf2jpg.Pdf2jpg(self)
        a.grid(row=1 , column=0 )
        
        b = gui_faxReceive.GUI_FaxReceive(self)
        b.grid(row=2 , column=0 , pady = 20)
        
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

        self.menu_list[0].append(FaxPdf(container))
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
        # self.wm_attributes("-topmost",1)
        self.title('웅천목재 프로그램 v.1')
        self.geometry('600x800+1850+10')


if __name__ == "__main__":
    app = App()
    ControlFrame(app)
    app.mainloop()
    
    