import tkinter as tk
from tkinter import ttk
import lib_calc_method as mcal
from tkinter import messagebox 
import sympy



        
class NumberSeparator:
    
    @staticmethod
    def setComma(val):
        return '{:,d}'.format(val) if val != 0 else ''
    
    @staticmethod    
    def rmComma(val):
        return val.replace(',','') if val != '' else ''
        

# class Calculotr

        
class CalculatorForTimber(): #수정된 코드
    def __init__(self, master):
        self.masterFrame = master
        self.totalPrice = {}
        
        self.frame_CalcTimber = tk.LabelFrame(self.masterFrame, text='목재 계산기')
        self.frame_CalcTimber.grid(row=0, column=0)
        
        self.type_on = True
        self.create_widgets()
        
    def create_widgets(self):
        # 엔트리 위젯을 담을 2차원 리스트 생성
        self.entry_widgets = []    #생성된 Entry를 배열로 저장함
        
        self.frame_top = tk.Frame(self.frame_CalcTimber)
        self.frame_top.grid(row=0,column=0, sticky='ew')
        
        add_button = tk.Button(self.frame_top, width=3 , justify='left', text="+", command=self.create_row)
        add_button.grid(row=0, column=0 , sticky='w')
        
        minus_button = tk.Button(self.frame_top, width=3 , justify='left', text="-", command=self.destroy_row)
        minus_button.grid(row=0, column=1, sticky='w')
        
        tk.Label(self.frame_top , text ='공급합계 : ', justify='right').grid(row=0,column=2, padx=15, sticky='e')
        self.totalCost = tk.Entry(self.frame_top, justify='left')
        # self.totalCost.bind('<FocusOut>', lambda event,key='totalCost' : self._handlrSetTotalData(event, key))
        self.totalCost.bind('<Return>', lambda event,key='totalCost' : self._handlrSetTotalData(event, key))
        self.totalCost.grid(row=0,column=3)
        
        tk.Label(self.frame_top , text ='운임합계 : ', justify='right').grid(row=0,column=4, padx=15, sticky='e')        
        self.transeCost = tk.Entry(self.frame_top, justify='left')
        # self.transeCost.bind('<FocusOut>', lambda event,key='transCost' : self._handlrSetTotalData(event, key))
        self.transeCost.bind('<Return>', lambda event,key='transCost' : self._handlrSetTotalData(event, key))
        self.transeCost.grid(row=0,column=5,padx=5) 
        
        self.title_list = ['NO.','Title', 'CalcQTY','QTY','TotalPrice','Price','TraceCost']
        # self.dataList = []
        
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
        
        self.btn_cal= tk.Button(self.frame_bottom, text='초기화' )
        self.btn_cal.grid(row=0,column=0,sticky='')
        
        tk.Label(self.frame_bottom , text ='총계확인: ').grid(row=0,column=1, padx=15, sticky='e') 
        self.checkTotalCost = tk.Entry(self.frame_bottom, justify='left', width=15)
        self.checkTotalCost.grid(row=0,column=2) 
        
        tk.Label(self.frame_bottom , text ='운임확인: ').grid(row=0,column=3, padx=15, sticky='e') 
        self.checkTransPort = tk.Entry(self.frame_bottom, width=15)
        self.checkTransPort.grid(row=0,column=4)
        
        self.btn_calc = ttk.Button(self.frame_bottom, text='계산',width=5, command=self._handlrCalCalculateAll).grid(row=0,column=5,padx=5)
        
    def create_row(self):
        # self.row_count += 1
        row_entries = []
        row_number = len(self.entry_widgets)
        # 엔트리 생성 및 라벨 추가
        
         # 각 행의 버튼 설정
        button = ttk.Button(self.frame_mid, text=f"{len(self.entry_widgets)}번 계산 ", command=lambda row=len(self.entry_widgets): self._handler_calc_line(row))
        button.grid(row=len(self.entry_widgets)+1, column=0)
        row_entries.append(button)

        
        for j in range(1,len(self.title_list),1):
            entry = ttk.Entry(self.frame_mid, width=10, justify='right')
            entry.grid(row=len(self.entry_widgets) + 1, column=j )
            
            entry.bind('<Return>', lambda event , row =row_number, col = j : self._handler_entry_enter(event, row, col))
            entry.bind('<Key>', lambda event, row= row_number, col = j :  self._handler_key_press(event,row,col ))
            row_entries.append(entry)
            
        self.entry_widgets.append(row_entries)

    def _printData(self, row, dataList):
        entryWidgets = self.entry_widgets[row]
        for i, e in enumerate(entryWidgets[1::1]):
            if i > 1 :
                self._printOneData(e,self.set_comma(dataList[i]))
            else : 
                self._printOneData(e,dataList[i])
    
    def _printOneData(self, widget, data):
        widget.delete(0,tk.END)
        widget.insert(0,data)
            
            
            
    def _handlrSetTotalData(self , e, key):
        thisData = e.widget.get()
        try : 
            thisData = int(thisData)
            self.totalPrice[key] = thisData
            e.widget.delete(0,tk.END)
            e.widget.insert(0,self.set_comma(thisData))
            
        except ValueError : 
            print('Put in only type of int')
    
    def _isCheckTotalData(self):
        
        try : 
            if self.totalPrice['totalCost'] > 0 and self.totalPrice['transCost'] > 0 :
                return True
        except TypeError : 
            return False
        except KeyError :
            return False 
    
    def _isCheckData(self,dataList, col):
        try : 
            if dataList[col] > 0 :
                return True
        except TypeError : 
            return False
    
    def rm_comma(self, str):
        return NumberSeparator.rmComma(str)
    
    def set_comma(self, str):
        return NumberSeparator.setComma(str)
    
    def _getDataFromListbox(self, row):
        thisDataList = []
        # [0]'NO.' [1]'Title', [2]'CalcQTY',[3]'QTY',[4]'TotalPrice',[5]'Price',[6]'TraceCost'
        for i in range(1, len(self.title_list), 1) :
            b= self.entry_widgets[row][i].get()
            try :
                thisDataList.append(int(self.rm_comma(b)) if b  != '' else 0)
            except ValueError :
                thisDataList.append(b)
                
        
        return thisDataList                 
    
    
    def _calculateByLine(self, data): 
        # [0]'Title', [1]'CalcQTY',[2]'QTY',[3]'TotalPrice',[4]'Price',[5]'TraceCost'
        dataFromList = data
        thisQty = dataFromList[2]
        thisTotalPrice = dataFromList[3]
        
        if thisQty != 0 and thisTotalPrice != 0 :
            dataFromList[4] = round(thisTotalPrice / thisQty)
            
            if len(self.totalPrice) != 0 :
                totalBuyingPrice = self.totalPrice['totalCost']
                totalTransPrice = self.totalPrice['transCost']

                if totalBuyingPrice.isdigit()  and  totalTransPrice.isdigit() :
                    totalBuyingPrice = int(totalBuyingPrice)
                    totalTransPrice = int(totalTransPrice)
                    
                    dataFromList[5] = (dataFromList[3]//totalBuyingPrice*totalTransPrice)//thisQty
                else : 
                    print("get result only price") 
            else :  
                print("there is no data")
        return dataFromList
    
    def _handlrCalCalculateAll(self):

        resultAllData = []
        
        for ix in range(len(self.entry_widgets)):
            dataFromList = self._getDataFromListbox(ix)
            if dataFromList[3] == 0:
                # continue
                resultAllData.append(dataFromList)
            else :
                resultAllData.append(self._calculateByLine(dataFromList))
        
        for ix in range(len(self.entry_widgets)):
            self._printData(ix, resultAllData[ix])
        
    def destroy_row(self):
        for w in self.entry_widgets[len(self.entry_widgets)-1]:
            w.destroy()
        
        self.entry_widgets.pop()
        
    # def get_transCostPer(self):
        
    #     totalCost = self.rm_comma(self.totalCost)
    #     transeCost = self.rm_comma(self.transeCost)
        
    #     if totalCost and  transeCost :
    #         return round( int(transeCost) / int(totalCost) ,5)
        
    #     else : False
    
    def _handler_calc_line(self,row ):
        
        thisDataList = self._getDataFromListbox(row)
        self._makeDataFunc(2 , thisDataList)
        # print(thisDataList)
        self._printData(row, thisDataList)
    
    
    
    def _calculateTransCost(self, dataList):
        try : 
            ((dataList[4] // self.totalPrice['totalCost']) * self.totalPrice['transCost']) // dataList[2]
        except KeyError : 
            pass        
        
    
    def _calcThreeToFive(self, thisDataList):
        # if self._isCheckData(thisDataList,3) != False:
        thisDataList[4] = thisDataList[3] // thisDataList[2]
        if self._isCheckTotalData() :
            thisDataList[5]= self._calculateTransCost(thisDataList)
        return thisDataList    

    def _makeDataFunc(self, numOfCol ,thisDataList):
        if numOfCol == 0 :
            pass
                  
        elif numOfCol == 1 :
            thisDataList[2]=self._calculatorByString(thisDataList[1])
            if self._isCheckData(thisDataList,3) != False:
                thisDataList = self._calcThreeToFive(thisDataList)
                  
        elif numOfCol == 2 :
             if self._isCheckData(thisDataList,3) != False:
                thisDataList = self._calcThreeToFive(thisDataList)
                  
        elif numOfCol == 3 :
            if self._isCheckData(thisDataList,2) != False : 
               self._calculateTransCost(thisDataList)
               thisDataList = self._calcThreeToFive(thisDataList)
                
        elif numOfCol == 4 :
            if self._isCheckData(thisDataList,2) != False : 
                thisDataList[3] = thisDataList[2] * thisDataList[4]
                if self._isCheckTotalData() :
                    thisDataList[5]= self._calculateTransCost(thisDataList)
        elif numOfCol == 5 :
            pass
        
        return thisDataList

    def _handler_entry_enter(self,e, row, col):
        '''intitialize data'''
        
        thisDataList = self._getDataFromListbox(row)
        self._makeDataFunc(col-1 , thisDataList)
        print(thisDataList)
        self._printData(row, thisDataList)

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
            
    def _calculatorByString(self,value):
        try : 
            return sympy.sympify(value)
        except ValueError :
            return value
    

    
class MarginCalculator():  # 수정중인 코드
    def __init__(self, frame):
        
        self.masterFrame = frame
        
        self.frameMarginCalc = tk.LabelFrame(self.masterFrame, text='마진계산기')
        self.frameMarginCalc.grid(row=0,column=0)

        self.type_on = True
        
        # self.separator = NumberSeparator()
        
        self.data_entry_list = {
            'buy_cost' : ['매입가'],
            'margin_rate' : ['마진율(%)'],
            'price' : ['공급가'],
            'price_tax' : ['부가세'],
            'price_wtax' : ['판매/tax'],
            'margin' : ['마진금'],
        }
        
        self.numberOfDatas = []
            
        self.create_widgets()
        
     
        
    def rm_comma(self, data):
        return NumberSeparator.rmComma(data) if str != '' else str
    
    def set_comma(self, str):
        return NumberSeparator.setComma(str)  if str != '' else str  
        
    def create_widgets(self):
        # 엔트리 위젯을 담을 2차원 리스트 생성
        self.entry_widgets = []
        # self.labels = ["Label"] + [f"Column {i}" for i in range(2, 7)]  # 열의 라벨
        
        for ix, title in enumerate(self.data_entry_list.values()):
            # label_text = self.labels[j]
            label = ttk.Label(self.frameMarginCalc, text=title)
            label.grid(row=0, column=ix+1)
        # 추가 버튼 생성
        add_button = ttk.Button(self.frameMarginCalc,width=7, text="Add Row", command=self.create_row)
        add_button.grid(row=0, column=0)
        for _ in range(5):
            self.create_row()  # 초기에 한 행 생성
            # self.DataSet.addInitList()
        # ttk.Button(self, text='test').grid(row= )
        
        
    def create_row(self):
        row_entries = []
        row_number = len(self.entry_widgets)
        # 엔트리 생성 및 라벨 추가
        for j in range(1, 7):
            entry = ttk.Entry(self.frameMarginCalc,width=10, justify='right')
            entry.grid(row=len(self.entry_widgets) + 1, column=j )
            
            entry.bind('<Return>', lambda event , row =row_number, col = j : self._handler_entry_enter(event, row, col))
            entry.bind('<Key>', lambda event, row= row_number, col = j :  self._handler_key_press(event,row,col ))
            row_entries.append(entry)
            
        self.entry_widgets.append(row_entries)

        # 각 행의 버튼 설정

        button = ttk.Button(self.frameMarginCalc, width= 7, text=f"VAT {len(self.entry_widgets)}", command=lambda row=len(self.entry_widgets)-1: self._buyPriceWithoutTax(row))
        button.grid(row=len(self.entry_widgets), column=0)
        
        button = ttk.Button(self.frameMarginCalc, width= 3, text=f"Re", command=lambda row=len(self.entry_widgets)-1: self._resetRow(row))
        button.grid(row=len(self.entry_widgets), column=8)
        
    def _buyPriceWithoutTax(self, row):
        getList = self._getDataFromListbox(row)
        
        getList[0] = round(getList[0] / 1.1) 
        
        self._printData(row, getList)
        

        
    def _resetRow(self, row):
        setZeroData = []
        for _ in range(len(self.data_entry_list)):
            setZeroData.append('')
        self._printData(row, setZeroData)
    
    def _printData(self, row, dataList):
        
        for i, e in enumerate(self.entry_widgets[row]):
            e.delete(0,tk.END)
            e.insert(0,self.set_comma(dataList[i]))  
          
    
    def _getDataFromListbox(self, row):
        thisDataList = []
        
        for i in range(len(self.data_entry_list)):
            b = self.entry_widgets[row][i].get()
            thisDataList.append(int(self.rm_comma(b)) if b  != '' else 0)
        
        return thisDataList         
            
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
        
    # def isBuyCost(self,row):
    #     self.entry_widgets[row][0].get()
      
        # print(thisDataList)
    
# ''' Enter Handler '''
    def _handler_entry_enter(self,e, row, col):  
        '''intitialize data'''
        
        NumberOfColum = col-1

        getDataList = self._getDataFromListbox(row)
        print(getDataList)
        listAfterCalc = []
        
        print(type(getDataList[0]))
        if NumberOfColum == 0 :   # 매입가
            if getDataList[1] != 0 or getDataList[1] != '':
                listAfterCalc = self._calc_by_margin_rate(getDataList)
            else : 
                for data in getDataList: 
                    listAfterCalc.append(0 if data == '' and data == 0  else int(data))
        else :
            if getDataList[0] > 0 or getDataList[0] != '' : 
                if NumberOfColum == 1 :  # 마진율
                    listAfterCalc = self._calc_by_margin_rate(getDataList)
                elif NumberOfColum == 2 :  # 공급가액
                    listAfterCalc = self._calc_by_price(getDataList)
                elif NumberOfColum == 3 :  # 부가세
                    for data in getDataList: 
                        listAfterCalc.append(0 if data == '' and data == 0  else int(data))
                
                elif NumberOfColum == 4 :  # 판매가 + 텍스
                    listAfterCalc = self._calc_by_price_wtax(getDataList)
                elif NumberOfColum == 5 :  # 마진금
                    listAfterCalc = self._calc_by_margin(getDataList)

        #    else  getDataList[0] == 0 or getDataList[0] == '' : 
            else : 
                messagebox.showwarning("Warning", "Required input Buy_cost")
                for data in getDataList: 
                    listAfterCalc.append(0 if data == '' and data == 0  else int(data))             
                    
        # print(listAfterCalc)
        self._printData(row,listAfterCalc)
         
    def _calc_by_price(self, dataList):
        data_list = dataList
        data_list[5] = data_list[2] - data_list[0]
        data_list[1] = round((data_list[5] / data_list[2]) * 100)
        data_list[3] = round(data_list[2] * 0.1)
        data_list[4] = data_list[2] + data_list[3]
        return data_list
    
    def _calc_by_price_wtax(self, dataList):
        data_list = dataList
        data_list[2] = round(data_list[4] / 1.1)
        data_list[5] =  data_list[2] - data_list[0]  
        data_list[1] = round((data_list[5] / data_list[2]) * 100)
        data_list[3] = round(data_list[2] * 0.1)
        return data_list
        
        
    def _calc_by_margin_rate(self, dataList):
        data_list = dataList
        data_list[2] = round(data_list[0] / (1-(data_list[1]/100)))
        data_list[5] =  data_list[2] - data_list[0]  
        data_list[3] = round(data_list[2] * 0.1)
        data_list[4] = data_list[2] + data_list[3]
        data_list = dataList
        return data_list

    def _calc_by_margin(self, dataList):
        data_list = dataList
        data_list[2] = data_list[0] + data_list[5]
        data_list[3] = round(data_list[2] * 0.1)
        data_list[4] = data_list[2] + data_list[3]
        data_list[1] = round((data_list[5] / data_list[2]) * 100)
        return data_list
    
class CalculatorCash():
    def __init__(self, master):
        # super().__init__(master)
        
        
        self.frameMaster = master
        self.mcal = mcal.MarginCalc()
        self.frame_Calc = tk.LabelFrame(self.frameMaster, text='현금계산기')
        self.frame_Calc.grid(row=0, column=0, padx= 10)
        self.type_on = True
        # self.master = master
        
        
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
        
        
        


class Calculators():
    def __init__(self, frame):
        self.masterFrame = frame
         
        self.frameMarginCalc = tk.Frame(self.masterFrame)
        self.frameMarginCalc.grid(row=0, column=0, padx= 10, pady=20)
        
        self.frameTimberCalc = tk.Frame(self.masterFrame)
        self.frameTimberCalc.grid(row=1, column=0, padx= 10, pady=20)

        self.frameCashCalc = tk.Frame(self.masterFrame)
        self.frameCashCalc.grid(row=2, column=0, pady=20 , sticky='w')
        
        MarginCalculator(self.frameMarginCalc)
        CalculatorForTimber(self.frameTimberCalc)
        CalculatorCash(self.frameCashCalc)
        
        
        
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('웅천목재 프로그램')
        self.geometry('600x800+1850+10')


if __name__ == "__main__":
    app = App()
    frameA = tk.Frame(app)
    Calculators(frameA)
    
    frameA.grid(row=0, column=0)
    app.mainloop()
            
        
     