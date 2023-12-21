import tkinter as tk
from tkinter import ttk
import lib_calc_method as mcal
from tkinter import messagebox 

class Calculator(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.mcal = mcal.MarginCalc()
        
        self.type_on = True
        self.master = master
        # self.grid()
        
        self.data_entry_list = {
            'buy_cost' : ['매입가'],
            'margin_rate' : ['마진율(%)'],
            'price' : ['공급가'],
            'price_tax' : ['부가세'],
            'price_wtax' : ['판매/tax'],
            'margin' : ['마진금'],
        }
        self.create_widgets()
    def create_widgets(self):
        # 엔트리 위젯을 담을 2차원 리스트 생성
        self.entry_widgets = []
        # self.labels = ["Label"] + [f"Column {i}" for i in range(2, 7)]  # 열의 라벨
        
        for ix, title in enumerate(self.data_entry_list.values()):
            # label_text = self.labels[j]
            label = ttk.Label(self, text=title)
            label.grid(row=0, column=ix+1)
        # 추가 버튼 생성
        add_button = ttk.Button(self, text="Add Row", command=self.create_row)
        add_button.grid(row=0, column=0)
        self.create_row()  # 초기에 한 행 생성
        
    def create_row(self):
        row_entries = []
        row_number = len(self.entry_widgets)
        # 엔트리 생성 및 라벨 추가
        for j in range(1, 7):
            entry = ttk.Entry(self,width=10, justify='right')
            entry.grid(row=len(self.entry_widgets) + 1, column=j )
            
            entry.bind('<Return>', lambda event , row =row_number, col = j : self._handler_entry_enter(event, row, col))
            entry.bind('<Key>', lambda event, row= row_number, col = j :  self._handler_key_press(event,row,col ))
            row_entries.append(entry)
            
        self.entry_widgets.append(row_entries)

        # 각 행의 버튼 설정
        button = ttk.Button(self, text=f"VAT {len(self.entry_widgets)}", command=lambda row=len(self.entry_widgets)-1: self.print_values(row))
        button.grid(row=len(self.entry_widgets), column=0)

    def print_values(self, row):
        # values = [int(entry.get()) for entry in self.entry_widgets[row][1:]]  # 첫 번째 라벨은 제외
        # print(f"Values in Row {row+1}: {values}")
        val  = self.entry_widgets[row][0].get()
        val = int(self._remove_separator(val)) if val else messagebox.showwarning("Warning", "Required input Buy_cost")
        val = round(val/1.1)
        self.entry_widgets[row][0].delete(0,tk.END)
        self.entry_widgets[row][0].insert(0,self._set_separator(val))
        
    
    def _set_separator(self,val):
        return '{:,d}'.format(val)
    
    def _remove_separator(self,val):
        if val :
            val = val.replace(',','')
            if val.isdigit():
                return val
            return False
        else :
            return False
            
    def _handler_key_press(self,event,row,col):
            
        if not self.type_on and event.char.isdigit():
            event.widget.delete(0,tk.END)
            self.type_on = True

            
    def _handler_entry_enter(self,e, row, col):
        '''intitialize data'''
        
        values = {}
        for i, e in enumerate(self.entry_widgets[row]):
            val = self._remove_separator(e.get())
            val = int(val) if val else 0
            
            if i == 0 and val == 0 :
                messagebox.showwarning("Warning", "Required input Buy_cost")
                return
            if i == 1 and int(val) > 99:
                messagebox.showwarning("Warning",'Please maintain a margin rate below 99%  ')
                return 
            values[i] = 0 if val == '' else int(val)
         
        self.mcal.priceList = values 
        
        if col == 2 : # calculate by margin rate
            self.mcal.calc_by_margin_rate()
        elif col == 3 : # calculate by price
            self.mcal.calc_by_price()
        elif col == 5 : # calculate by price with tax
            self.mcal.calc_by_price_wtax()
        elif col == 6: # calculate by margin
            self.mcal.calc_by_margin()
        
        for i, e in enumerate(self.entry_widgets[row]):
            e.delete(0,tk.END)
            e.insert(0,self._set_separator(self.mcal.priceList[i]))    
            
        self.type_on = False
        
class MainApplication(tk.Tk):
    def __init__(self,container):
        super().__init__(container)

        self.a_frame = A(self)
        self.a_frame.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
