
import tkinter as tk
from tkinter import ttk
from tkinter import * # __all__
import PIL
import math


import gui_calculator
import gui_Utilities
import gui_pdf2jpg
import win32clipboard
import settingFille


        
class ControlFrame():
    def __init__(self, root):
        # super().__init__(container)
   
        self.root = root
        self.topMenuFrame = Frame(self.root)
        self.contentFaxFrame = Frame(self.root)
        self.contentMarginCalc = Frame(self.root)
        self.settings = Frame(self.root)
        
        gui_Utilities.Utilities(self.contentFaxFrame)
        gui_calculator.Calculators(self.contentMarginCalc)
        settingFille.SettingsApp(self.settings)
        self.menu_list = {
            0 : ['컨버터 및 팩스'],
            1 : ['마진 계산기'],
            2 : ['설정']
        }
        self.NUMBER_TITLE = 0
        self.NUMBER_FRAME = 1
        
        for ix , key in enumerate(self.menu_list.keys()):
            e = Button(self.topMenuFrame , text=self.menu_list[key][self.NUMBER_TITLE],command=lambda x=key: [self.change_frame(x)])
            e.grid(row=0, column=ix)
            
            # Button(f , text='app2',command=lambda x=1 : self.change_frame(x)).grid(row=0, column=1)
            
        self.topMenuFrame.grid(row=0, column=0 , sticky='w' , pady=20)
        
        # self.grid(column=0, row=0, padx=5, pady=5, sticky='ew')
        
        self.frames = {}

        self.menu_list[0].append(self.contentFaxFrame)
        self.menu_list[1].append(self.contentMarginCalc)
        self.menu_list[2].append(self.settings)
        
        self.current_frame = self.menu_list[0][self.NUMBER_FRAME]
        self.change_frame(0)
        
        
    def change_frame(self,x):
        # print(x)
        self.current_frame.grid_forget()
        self.current_frame = self.menu_list[x][self.NUMBER_FRAME]
        self.current_frame.grid(row =1, column=0)
        

if __name__ == "__main__":
    app = tk.Tk()
    app.title('웅천목재 프로그램 v.1')
    app.geometry('600x800+1850+10')
    ControlFrame(app)
        
    app.mainloop()
    
    