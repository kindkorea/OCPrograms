import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import * # __all__
import math

class Calc_margins(Frame):
    def __init__(self, master, column_list, cell_width):
        super().__init__(master)

        self.col_value = column_list
        self.low_value = ['Price','w/Tax','Earning']    
        self.width = cell_width
        self.list_entry = {}
        self.data_entry = {}
        self.__initialize()

    def __initialize(self):

        self.__make_entry(0,0,self.width,5000,True).bind('<Return>' , self.__set_cells)

        for row in range(len(self.low_value)):  # make menu row
            self.__make_entry(row+1, 0, self.width, f'{self.low_value[row]}',False)

        for column , key in enumerate(self.col_value): # make data cell
            self.__make_btn(0, column+1, self.width, key) 
            for row in range(len(self.low_value)):
               self.list_entry[key] = self.__make_entry(row+1, column+1, self.width, '' , True)

        
        

    def __make_entry(self, row, column, width, text, state):
        e = Entry(self, width=width)
        if text: e.insert(0, text)
        e['state'] = NORMAL if state else DISABLED
        e.coords = (row-1, column-1)
        e.grid(row=row, column=column)
        return e
    
    def __make_btn(self, row, column, width, text):
        e = Button(self, width=width , text = f'Margin {text}%' , command= lambda : self.__btn_cell_data(text))
        e.coords = (row-1, column-1)
        e.grid(row=row, column=column)
        return e

    def __set_cells(self, event):
        
        get_cost = event.widget.get()

        data = self.__get_calc(int(get_cost))

        for i ,e in enumerate(self.list_entry):
            e.delete(0,END)
            e.insert(END,data[i])

    def __btn_cell_data(self,text):
        # print(event)
        print(text)

    def __get_calc(self, cost):
        for margin in self.col_value:
            cost_price = math.trunc(round(cost / (1- margin/100), -2))
            cost_margin = cost_price - cost
            price_with_tax = math.trunc(cost_price * 1.1)
            self.data_entry[margin]= '{:,}'.format(cost_price)
            self.data_entry[margin] = '{:,}'.format(price_with_tax)
            self.data_entry[margin] = '{:,}'.format(cost_margin)
     



class Calc_margin(Frame):
    def __init__(self, master, cell_width):
        super().__init__(master)    

        self.width = cell_width
        self.menu_list = ['BuyingCost', 'TransCost','Price','w/Price','Earning','MarginRate']

        for i, e in enumerate(self.menu_list):
            self.__make_entry(6,i,self.width,e,False)

        self.buying_cost = self.__make_entry(7,0,self.width,'',True)
        self.buying_cost.bind('<Return>',self.__calc_buying_cost)
        self.transport_cost = self.__make_entry(7,1,self.width,'',True)
        self.price = self.__make_entry(7,2,self.width,'',True)
        self.wPrice = self.__make_entry(7,3,self.width,'',True)
        self.earing = self.__make_entry(7,4,self.width,'',True)
        self.margin_rate = self.__make_entry(7,5,self.width,'',True)

    def __calc_buying_cost(self,event):
        print(event)
    def __make_entry(self, row, column, width, text, state):
        e = Entry(self, width=width)
        if text: e.insert(0, text)
        e['state'] = NORMAL if state else DISABLED
        e.coords = (row-1, column-1)
        e.grid(row=row, column=column)
        return e
    
app = Tk()
margin_list = [15,20,25,30,35,40]
ex = Calc_margins(app, margin_list , 12)
ex.pack(padx=20, pady=20)

ex2 = Calc_margin(app,12)
ex2.pack(padx=20, pady=20 ,side = 'left')


app.mainloop()
