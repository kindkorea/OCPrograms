import tkinter as tk
from tkinter import ttk
import lib_calc_method as mcal
from tkinter import messagebox 
import sympy

class MySeparator:
    def set_separator(self,val):
            return '{:,d}'.format(val)
        
    def remove_separator(self,val):
        if val :
            val = val.replace(',','')
            if val.isdigit():
                return val
            return False
        else :
            return False



        
class CalculatorForTimber(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.frame_CalcTimber = tk.LabelFrame(self, text='목재 계산기')
        self.frame_CalcTimber.grid(row=0, column=0)
        
        self.type_on = True
        self.separator = MySeparator()
        
        self.row_count = 0
        self.create_widgets()
        
    def create_widgets(self):
        # 엔트리 위젯을 담을 2차원 리스트 생성
        self.entry_widgets = []
        self.frame_top = tk.Frame(self.frame_CalcTimber)
        self.frame_top.grid(row=0,column=0, sticky='ew')
        
        add_button = tk.Button(self.frame_top, width=3 , justify='left', text="+", command=self.create_row)
        add_button.grid(row=0, column=0 , sticky='w')
        
        add_button = tk.Button(self.frame_top, width=3 , justify='left', text="-", command=self.destroy_row)
        add_button.grid(row=0, column=1, sticky='w')
        
        tk.Label(self.frame_top , text ='총금액 : ', justify='right').grid(row=0,column=2, padx=15, sticky='e') 
        self.totalCost = tk.Entry(self.frame_top, justify='left')
        self.totalCost.grid(row=0,column=3) 
        
        tk.Label(self.frame_top , text ='운반비 : ', justify='right').grid(row=0,column=4, padx=15, sticky='e')        
        self.transeCost = tk.Entry(self.frame_top, justify='left')
        self.transeCost.grid(row=0,column=5,padx=5) 
        
        self.title_list = ['품목', '수량계산기','수량','공급가액','금액/단위','운반비/단위']
        
        
        self.frame_mid = tk.Frame(self.frame_CalcTimber)
        self.frame_mid.grid(row=1,column=0)
        for ix, title in enumerate(self.title_list):
            l = tk.Label(self.frame_mid, text=title , justify='center')
            # l.config('width',100) 
            l.grid(row=0, column=ix)
            
        for _ in range(5):
            self.create_row()
        
        self.frame_bottom = tk.Frame(self.frame_CalcTimber)
        self.frame_bottom.grid(row=2,column=0)
        
        self.btn_cal= ttk.Button(self.frame_bottom, text='삭제',width=5 ).grid(row=0,column=0)
        
        
        tk.Label(self.frame_bottom , text ='확인 총금액 : ').grid(row=0,column=1, padx=15, sticky='e') 
        self.checkTotalCost = tk.Entry(self.frame_bottom, justify='left', width=15)
        self.checkTotalCost.grid(row=0,column=2) 
        
        tk.Label(self.frame_bottom , text ='확인 운반비 : ').grid(row=0,column=3, padx=15, sticky='e') 
        self.checkTransPort = tk.Entry(self.frame_bottom, width=15)
        self.checkTransPort.grid(row=0,column=4)
        

        
        self.btn_calc = ttk.Button(self.frame_bottom, text='계산',width=5, command=self._cal_calculate112).grid(row=0,column=5,padx=5)
        
        
    def rm_comma(self, widget):
        return self.separator.remove_separator(widget.get())
    
    def set_comma(self, str):
        return self.separator.set_separator(str)
    
            
    
    def _cal_calculate112(self):

        transCostPer =  self.get_transCostPer()
        checkTotalCost = 0
        checkTransCost = 0 
        if transCostPer:
            for widgets in self.entry_widgets:
                
                cost = self.rm_comma(widgets[4])
                quantity = self.rm_comma(widgets[2])
                
                if cost and quantity:
                    
                    transPer = transCostPer * int(cost)
                    widgets[5].delete(0,tk.END)
                    widgets[5].insert(0,self.set_comma(round(transPer)))

            
                    checkTotalCost += int(cost) * int(quantity)
                    checkTransCost += int(quantity) * transPer
                    
        self.checkTotalCost.delete(0,tk.END)
        self.checkTotalCost.insert(0,self.set_comma(round(checkTotalCost)))
        
        self.checkTransPort.delete(0,tk.END)
        self.checkTransPort.insert(0,self.set_comma(round(checkTransCost)))
                    
                    
                    

        
    def destroy_row(self):
        for w in self.entry_widgets[self.row_count - 1]:
            w.destroy()
        
        self.row_count -= 1
        
        
    def create_row(self):
        self.row_count += 1
        row_entries = []
        row_number = len(self.entry_widgets)
        # 엔트리 생성 및 라벨 추가
        for j in range(len(self.title_list)):
            entry = ttk.Entry(self.frame_mid, width=10, justify='right')
            entry.grid(row=len(self.entry_widgets) + 1, column=j )
            
            entry.bind('<Return>', lambda event , row =row_number, col = j : self._handler_entry_enter(event, row, col))
            entry.bind('<Key>', lambda event, row= row_number, col = j :  self._handler_key_press(event,row,col ))
            row_entries.append(entry)
            
        self.entry_widgets.append(row_entries)

        # 각 행의 버튼 설정
        button = ttk.Button(self.frame_mid, text=f"계산 {len(self.entry_widgets)}", command=lambda row=len(self.entry_widgets)-1: self._handler_calc_line(row))
        button.grid(row=len(self.entry_widgets), column=6)
        self.entry_widgets.append(button)

    def get_transCostPer(self):
        
        totalCost = self.rm_comma(self.totalCost)
        transeCost = self.rm_comma(self.transeCost)
        
        if totalCost and  transeCost :
            return round( int(transeCost) / int(totalCost) ,5)
        
        else : False

    def _handler_calc_line(self,row ):
        quantity = self.rm_comma(self.entry_widgets[row][2])
        toto_cost = self.rm_comma(self.entry_widgets[row][3])
        
        if quantity and toto_cost : 
            
            quantity = int(quantity)
            toto_cost = int(toto_cost)
            
            result = round(toto_cost/quantity)
            
            self.entry_widgets[row][4].delete(0,tk.END)
            self.entry_widgets[row][4].insert(0,self.set_comma(result))
            
            transCostPer = self.get_transCostPer()
            if transCostPer :        
                self.entry_widgets[row][5].insert(0,self.set_comma(round(transCostPer * result)))
        else : 
            print('input require value')    
        
        
        
    
    def _handler_entry_enter(self,e, row, col):
        '''intitialize data'''
        
        if col == 1 : # quantity calculator 
            value = self._cal_calculate(e.widget.get())
            self.entry_widgets[row][2].delete(0,tk.END)
            self.entry_widgets[row][2].insert(0,self.set_comma(int(value)))
            
            
        elif col == 3 : # purchase cost
            totalCost = self.rm_comma(e.widget)
            e.widget.delete(0,tk.END)
            e.widget.insert(0,self.set_comma(int(totalCost)))
            
            
            quantity = self.rm_comma(self.entry_widgets[row][2])
            
            if not quantity:
                self.entry_widgets[row][1].focus()
            else : 
                
                # quantity = self.set_comma(self.entry_widgets[row][3])
                result = int(totalCost) / int(quantity)
                self.entry_widgets[row][4].delete(0,tk.END)
                self.entry_widgets[row][4].insert(0,self.set_comma(int(result)))



    def _handler_key_press(self, e, row, col):  # move cursor
        keyCode = e.keycode
        r_row = row
        r_col = col
        
        number_row = len(self.entry_widgets)
        number_col = len(self.title_list)
        
        if keyCode == 37:  # arrow key : left
            r_col = (r_col -1) % number_col
        elif keyCode == 38: # arrow key : top
            r_row = (r_row -1) % number_row
        elif keyCode == 39: # arrow key : right
            r_col = (r_col +1) % number_col
        elif keyCode == 40: # arrow key : bottom
            r_row = (r_row +1) % number_row
        
        self.entry_widgets[r_row][r_col].focus_set()
            
    
    
    
    def _cal_calculate(self,value):
        return sympy.sympify(value)
        

        


    
class Calculator(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.mcal = mcal.MarginCalc()
        self.frame_marginCalc = tk.LabelFrame(self, text='마진계산기')
        self.frame_marginCalc.grid(row=0, column=0, padx= 10)
        self.type_on = True
        self.master = master
        
        self.separator = MySeparator()
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
        
        calTimber = CalculatorForTimber(self)
        
        calTimber.grid(row=1, column=0,  padx=10 , pady= 20,sticky='ew')
        CalculatorCash(self).grid(row=2, column=0,padx=10 , pady= 20,sticky='ew')
        
    def rm_comma(self, widget):
        return self.separator.remove_separator(widget.get())
    
    def set_comma(self, str):
        return self.separator.set_separator(str)    
        
    def create_widgets(self):
        # 엔트리 위젯을 담을 2차원 리스트 생성
        self.entry_widgets = []
        # self.labels = ["Label"] + [f"Column {i}" for i in range(2, 7)]  # 열의 라벨
        
        for ix, title in enumerate(self.data_entry_list.values()):
            # label_text = self.labels[j]
            label = ttk.Label(self.frame_marginCalc, text=title)
            label.grid(row=0, column=ix+1)
        # 추가 버튼 생성
        add_button = ttk.Button(self.frame_marginCalc, text="Add Row", command=self.create_row)
        add_button.grid(row=0, column=0)
        for _ in range(5):
            self.create_row()  # 초기에 한 행 생성
        # ttk.Button(self, text='test').grid(row= )
        
        
    def create_row(self):
        row_entries = []
        row_number = len(self.entry_widgets)
        # 엔트리 생성 및 라벨 추가
        for j in range(1, 7):
            entry = ttk.Entry(self.frame_marginCalc,width=10, justify='right')
            entry.grid(row=len(self.entry_widgets) + 1, column=j )
            
            entry.bind('<Return>', lambda event , row =row_number, col = j : self._handler_entry_enter(event, row, col))
            entry.bind('<Key>', lambda event, row= row_number, col = j :  self._handler_key_press(event,row,col ))
            row_entries.append(entry)
            
        self.entry_widgets.append(row_entries)

        # 각 행의 버튼 설정
        button = ttk.Button(self.frame_marginCalc, text=f"VAT {len(self.entry_widgets)}", command=lambda row=len(self.entry_widgets)-1: self.print_values(row))
        button.grid(row=len(self.entry_widgets), column=0)

    def print_values(self, row):
        # values = [int(entry.get()) for entry in self.entry_widgets[row][1:]]  # 첫 번째 라벨은 제외
        # print(f"Values in Row {row+1}: {values}")
        val  = self.rm_comma(self.entry_widgets[row][0])
        val = int(val) if val else messagebox.showwarning("Warning", "Required input Buy_cost")
        val = round(val/1.1)
        self.entry_widgets[row][0].delete(0,tk.END)
        self.entry_widgets[row][0].insert(0,self.set_comma(val))
    
            
    def _handler_key_press(self,event,row,col):
            
        if not self.type_on and event.char.isdigit():
            event.widget.delete(0,tk.END)
            self.type_on = True
            
        keyCode = event.keycode
        r_row = row
        r_col = col-1
        
        number_row = len(self.entry_widgets)
        number_col = len(self.data_entry_list)
        
        if keyCode == 37:  # arrow key : left
            r_col = (r_col -1) % number_col
        elif keyCode == 38: # arrow key : top
            r_row = (r_row -1) % number_row
        elif keyCode == 39: # arrow key : right
            r_col = (r_col +1) % number_col
        elif keyCode == 40: # arrow key : bottom
            r_row = (r_row +1) % number_row
        
        self.entry_widgets[r_row][r_col].focus_set()
        

            
    def _handler_entry_enter(self,e, row, col):
        '''intitialize data'''
        
        values = {}
        for i, widget in enumerate(self.entry_widgets[row]):
            val = self.rm_comma(widget)
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
            
            
        # def _handler_key_press(self, e, row, col):  # move cursor
        
        
        
        
        for i, e in enumerate(self.entry_widgets[row]):
            e.delete(0,tk.END)
            e.insert(0,self.set_comma(self.mcal.priceList[i]))    
            
        self.type_on = False




class CalculatorCash(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.mcal = mcal.MarginCalc()
        self.frame_Calc = tk.LabelFrame(self, text='현금계산기')
        self.frame_Calc.grid(row=0, column=0, padx= 10)
        self.type_on = True
        self.master = master
        
        
        self.data_entry_list = ['오만원','만원','오천원','천원','총합계']
            
        
        self.create_widgets()
        
        # 각 행의 버튼 설정
        
        button = ttk.Button(self.frame_Calc, text='초기화', command=self.reset_input_data)
        button.grid(row=0, column=0)
        
        
        button = ttk.Button(self.frame_Calc, text='계산 하기', command=self.calculate)
        button.grid(row=1, column=0)
        
        
    def create_widgets(self):
        # 엔트리 위젯을 담을 2차원 리스트 생성
        self.entry_widgets = []
        # self.labels = ["Label"] + [f"Column {i}" for i in range(2, 7)]  # 열의 라벨
        
        for ix, title in enumerate(self.data_entry_list):
            # label_text = self.labels[j]
            label = ttk.Label(self.frame_Calc, text=title)
            label.grid(row=0, column=ix+1)
        
        for _ in range(2):
            self.create_row()
        
        
    def create_row(self):
        row_entries = []
        row_number = len(self.entry_widgets)
        # 엔트리 생성 및 라벨 추가
        for j in range(1, len(self.data_entry_list)+1):
            entry = ttk.Entry(self.frame_Calc, width=10, justify='right')
            entry.grid(row=len(self.entry_widgets) + 1, column=j )
            
            entry.bind('<Return>',  self._handler_entry_enter)
            entry.bind('<Key>', lambda event, row= row_number, col = j :  self._handler_key_press(event,row,col ))
            row_entries.append(entry)
            
        self.entry_widgets.append(row_entries)

        
    def reset_input_data(self):
        for widget in self.entry_widgets:
            for w in widget:
                w.delete(0,tk.END)
    
    def calculate(self):
        total_per_cash = []
        cash_count = int()
        cash_amount = [50000,10000,5000,1000]
        total_cash = int()
        
        
        for ix, cash in enumerate(cash_amount):
            getdata = self.entry_widgets[0][ix].get()
            get_count = int()
            if getdata == '':
                get_count = 0
            else : 
                get_count = int(getdata)
            cash_count += get_count
            
            calc_cash = get_count * cash
            total_per_cash.append(calc_cash)
            total_cash += calc_cash
            
        total_per_cash.append(total_cash)
        
        self.entry_widgets[0][4].delete(0,tk.END)
        self.entry_widgets[0][4].insert(0,'{:,d}'.format(cash_count))
        widget = self.entry_widgets[1]
        for ix , cash in enumerate(total_per_cash):
            widget[ix].delete(0,tk.END)
            widget[ix].insert(0,'{:,d}'.format(cash))
        
   
    def _handler_key_press(self,event,row,col):
        pass
        # if not self.type_on and event.char.isdigit():
        #     event.widget.delete(0,tk.END)
        #     self.type_on = True
            
        # keyCode = event.keycode
        # r_row = row
        # r_col = col-1
        
        # number_row = len(self.entry_widgets)
        # number_col = len(self.data_entry_list)
        
        # if keyCode == 37:  # arrow key : left
        #     r_col = (r_col -1) % number_col
        # elif keyCode == 38: # arrow key : top
        #     r_row = (r_row -1) % number_row
        # elif keyCode == 39: # arrow key : right
        #     r_col = (r_col +1) % number_col
        # elif keyCode == 40: # arrow key : bottom
        #     r_row = (r_row +1) % number_row
        
        # self.entry_widgets[r_row][r_col].focus_set()
        
    
    def _handler_entry_enter(self,e):
        '''intitialize data'''
        self.calculate()
        
        
        
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('웅천목재 프로그램')
        self.geometry('600x800+1850+10')


if __name__ == "__main__":
    app = App()
    CalculatorCash(app).grid(row=0,column=0)
    app.mainloop()
            
        
     