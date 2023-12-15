import tkinter as tk
from tkinter import ttk
from tkinter import * # __all__
import math



class Calculator(Frame):
    def __init__(self, container, row, col):
        super().__init__(container)
        
        # self.grid(column=col,row=row)
        
        self.data_entry_list = {
            'buy_cost' : ['매입가'],
            'margin_rate' : ['마진율(%)'],
            'price' : ['공급가'],
            'price_tax' : ['부가세'],
            'price_wtax' : ['판매/tax'],
            'margin' : ['마진금'],
        }
        
        
        self.CELL_WIDTH = 10
        self.ENTER_ON = True
        self.buy_cost = 0
        self.margin_rate = 0
        self.price = 0
        self.price_tax = 0
        self.price_wtax = 0
        self.margin = 0
        self.taxCheckVar = IntVar()
        
        
        self.__create_widgets()
        
    def __create_widgets(self):
        
        # for ix in range(len(self.data_list)):
        #     self.__make_entry(0,ix,self.data_list[ix],FALSE)
       
        checkbutton1= Button(self, text='Change', command=self.__handler_without_tax)
        checkbutton1.grid(row=0,column=0,rowspan=2, sticky='sn')
        
        for ix, name in enumerate(self.data_entry_list.values()):
            self.__make_entry(0,ix+1,self.CELL_WIDTH,name[0],FALSE)
        
        
        for ix, key in enumerate(self.data_entry_list.keys()):
            self.data_entry_list[key].append( self.__make_entry(1, ix+1, self.CELL_WIDTH,'',TRUE))
        
        print(self.data_entry_list)
        # self.input_entry_list.reverse()


    def __make_entry(self, row, column,width, text, state):
        e = Entry(self, width=width)
        if text: e.insert(0, text)
        e['state'] = NORMAL if state else DISABLED
        e['justify'] = 'right' if state else 'center'
        e.coords = (row-1, column-1)
        # e.bind('<Return>', lambda  column : self.__handler_entry_enter(column))
        e.bind('<Return>', self.__handler_entry_enter)
        e.bind('<Key>', self.__handler_enter_key)
        e.grid(row=row, column=column)
        return e

    def __get_widget_key(self, widget):
        for  k in self.data_entry_list.keys():
            if self.data_entry_list[k][1] == widget:
                return k
    
    def __handler_without_tax(self):
        # if self.taxCheckVar.get() == TRUE:
        self.buy_cost = self.__remove_separator(self.data_entry_list['buy_cost'][1].get())
        
        if self.buy_cost != None :
            self.buy_cost  = round(self.buy_cost / 1.1)
            self.data_entry_list['buy_cost'][1].delete(0,END)
            self.data_entry_list['buy_cost'][1].insert(0,self.buy_cost)
        
    def __handler_enter_key(self,e):
        if self.ENTER_ON and e.keycode != 9:
            w_key = self.__get_widget_key(e.widget)    
            print(f'__handler_enter_key : {w_key=}')
            self.data_entry_list[w_key][1].delete(0,END)
            self.ENTER_ON = False
        
    def __handler_entry_enter(self,e):
        '''intitialize data'''
        self.ENTER_ON = True
        self.buy_cost = self.__remove_separator(self.data_entry_list['buy_cost'][1].get())
        
        self.margin_rate = 0
        self.price = 0
        self.price_tax = 0
        self.price_wtax = 0
        self.margin = 0
        
        w_key = self.__get_widget_key(e.widget)
        entry_data = int(e.widget.get())
        print(type(entry_data))
        
        if w_key == 'price' :
            self.__calc_by_price(entry_data)
        elif w_key == 'margin_rate' :
            self.__calc_by_margin_rate(entry_data)
        elif w_key == 'margin' :
            self.__calc_by_margin(entry_data)
        elif w_key == 'price_wtax' :
            self.__calc_by_price_wtax(entry_data)
        
        self.marginCalc_print()
        
        
    
    
    
    def __calc_by_price_wtax(self, price_wtax):
        print(f'__calc_by_margin_rate{price_wtax=}')
        self.price_wtax = price_wtax
        self.price_tax = round(self.price_wtax / 11)
        self.price = self.price_wtax - self.price_tax
        self.margin = self.price - self.buy_cost
        self.margin_rate = round((self.margin / self.price) * 100)
            
    def __calc_by_margin_rate(self,margin_rate):
        print(f'__calc_by_margin_rate{margin_rate=}')
        self.margin_rate = margin_rate
        self.price = round(self.buy_cost / (1-(margin_rate/100)))
        self.price_tax = round(self.price * 0.1)
        self.price_wtax = self.price + self.price_tax
        self.margin = self.price - self.buy_cost
        
        
        
    def __calc_by_margin(self,margin):
        print(f'__calc_by_margin {margin=}')
        self.margin = margin
        self.price = round(self.buy_cost + self.margin)
        self.margin_rate = round((self.margin / self.price) * 100)
        self.price_tax = round(self.price * 0.1)
        self.price_wtax = self.price + self.price_tax
        
        
    def __calc_by_price(self,price):
        print(f'__calc_by_price {price=}')
        self.price = price
        self.margin =  self.price  - self.buy_cost
        self.margin_rate = round((self.margin / self.price) * 100)
        self.price_tax = round(self.price * 0.1)
        self.price_wtax = self.price + self.price_tax

    def __set_separator(self,val):
        return '{:,d}'.format(val)
    
    def __remove_separator(self,val):
        if val != '':
            return int(val.replace(',',''))
            
            
            
    def marginCalc_print(self):
        for e in self.data_entry_list.values():
            e[1].delete(0,END)
        
        self.data_entry_list['buy_cost'][1].insert(0,self.__set_separator(self.buy_cost))
        self.data_entry_list['margin_rate'][1].insert(0,self.__set_separator(self.margin_rate))
        self.data_entry_list['price'][1].insert(0,self.__set_separator(self.price))
        self.data_entry_list['price_tax'][1].insert(0,self.__set_separator(self.price_tax))
        self.data_entry_list['price_wtax'][1].insert(0,self.__set_separator(self.price_wtax))
        self.data_entry_list['margin'][1].insert(0,self.__set_separator(self.margin))
        
        
        print(f'{self.buy_cost=}')
        print(f'{self.margin_rate=}')
        print(f'{self.price=}')
        print(f'{self.price_tax=}')
        print(f'{self.price_wtax=}')
        print(f'{self.margin=}')
        # for entry in self.input_entry_list:
        #     entry.delete(0,END)
        
        # self.input_entry_list[0].insert(0,self.buy_cost)
        # self.input_entry_list[1].insert(0,self.price)
        # self.input_entry_list[2].insert(0,self.margin_rate)
        # self.input_entry_list[3].insert(0,self.margin)
        # self.input_entry_list[4].insert(0,self.price_tax)
        # self.input_entry_list[5].insert(0,self.price_wtax)
        
        
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
        fax_receive = Calculator(self)
        fax_receive.grid(column=0, row=1)
        # # create the button frame
        # button_frame = gui_pdf2jpg.Cb_Btn_frame(self,8)

        
if __name__ == "__main__":
    app = App()
    app.mainloop()        