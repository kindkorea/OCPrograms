import tkinter as tk
from tkinter import ttk
from tkinter import * # __all__
import math
import string


class TransportCharge(Frame):
    def __init__(self, container):
        super().__init__(container)
        
        self.xAxis = string.ascii_lowercase[0:2]
        self.yAxis = range(0, 2)
        

        
        self.__create_widgets()
        
    def __create_widgets(self):
        
        
        self.count_line = 2
        self.top_frame = Frame(self)
        self.top_frame.grid(row=0,column=0, pady=10 ,sticky='w')
        
        Button(self.top_frame, text='VAT', command=lambda :  [self.__handler_btn_tax(100)]).grid(row=0, column=0)
        
        Label(self.top_frame, text = 'Total :').grid(row=0, column=1)
        
        self.total_cost = Entry(self.top_frame) 
        self.total_cost.grid(row=0, column=2)
        
        
        Label(self.top_frame, text = 'TransCharge :').grid(row=0, column=3)
        self.transport_cost = Entry(self.top_frame) 
        self.transport_cost.grid(row=0, column=4)
        
        Button(self.top_frame, text='+', command=self.__handler_btn_plus_line).grid(row=0, column=5)
        
        self.mid_frame = Frame(self)
        self.mid_frame.grid(row=1,column=0, sticky='w')
        self.draw_set(self.mid_frame)
        Button(self.mid_frame, text='VAT', command=self.__handler_btn_tax).grid(row=0, column=0, sticky='ew') 
        Button(self.mid_frame, text='Calculate', command=self.run_calc , bg='white').grid(row=0, column=1, columnspan=2, sticky='ew') 
        # Label(self.mid_frame, text='', width=5, background='white' ).grid(row=y ,column=0)
        
        
    def run_calc(self):
        print('run_calc')
    
    def draw_set(self,container):
        for y in self.yAxis: 
            Label(container, text=y, width=5, background='white' ).grid(row=y+1 ,column=0)
            for xcoor, x in enumerate(self.xAxis):
                key = f'{x}{y}'
                e = Entry(container)
                e.grid(row=y+1, column=xcoor+1)
        
        
    def __handler_btn_plus_line(self):
        
        self.draw_set(self.count_line, )
        self.count_line += 1 
    
    
    def __handler_btn_tax(self,index):
        print(f'__handler_btn_tax{index}')
        
class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Replace')
        self.geometry('500x500+2000+100')
        # self.resizable(0, 0)
        # windows only (remove the minimize/maximize button)
        # self.attributes('-toolwindow', True)

        # layout on the root window
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        # create the input frame
        # input_frame = gui_pdf2jpg.Pdf2jpg(self,8)
        # input_frame.grid(column=0, row=0)
        fax_receive = TransportCharge(self)
        fax_receive.grid(column=0, row=1)
        # # create the button frame
        # button_frame = gui_pdf2jpg.Cb_Btn_frame(self,8)

        
if __name__ == "__main__":
    app = App()
    app.mainloop()        