import math



class MatrixDataSet():
    def __init__(self,numberOfItems):

        self.data_list = []
        self.numberOfColumn = numberOfItems
    @property
    def getData(self):
        return self.data_list
    
    @property
    def dataListLen(self):
        return len(self.data_list)

    def addInitList(self):
        self.data_list.append([0]*self.numberOfColumn)
        
    def resetData(self, row):
        for i in range(self.numberOfColumn):
            self.data_list[row][i] = 0
        
    def delData(self, row):
        del self.data_list[row] 
    
    def setData(self,row,col,data):
        self.data_list[row][col] = data


class MarginCalculator():
    def __init__(self,initialNumbers):
        self.dataList = MatrixDataSet(5)
        '''
            buy_cost = 0
            margin_rate = 1
            price = 2
            price_tax = 3
            price_wtax = 4
            margin = 5
        '''
        
        for i in range(initialNumbers):
            self.dataSet.addInitList()
            
    def calculate(self, row, col):
        rowData = self.dataList.getData[row]
        
        
    

    
    # def calc_by_price(self,row):
    #     if(self.data_list[])
    #     self.data_list[5] = self.data_list[2] - self.data_list[0]
    #     self.data_list[1] = round((self.data_list[5] / self.data_list[2]) * 100)
    #     self.data_list[3] = round(self.data_list[2] * 0.1)
    #     self.data_list[4] = self.data_list[2] + self.data_list[3]
    
    # def calc_by_price_wtax(self):
    #     self.data_list[2] = round(self.data_list[4] / 1.1)
    #     self.data_list[5] =  self.data_list[2] - self.data_list[0]  
    #     self.data_list[1] = round((self.data_list[5] / self.data_list[2]) * 100)
    #     self.data_list[3] = round(self.data_list[2] * 0.1)
        
    # def calc_by_margin_rate(self):
    #     self.data_list[2] = round(self.data_list[0] / (1-(self.data_list[1]/100)))
    #     self.data_list[5] =  self.data_list[2] - self.data_list[0]  
    #     self.data_list[3] = round(self.data_list[2] * 0.1)
    #     self.data_list[4] = self.data_list[2] + self.data_list[3]

    # def calc_by_margin(self):
    #     self.data_list[2] = self.data_list[0] + self.data_list[5]
    #     self.data_list[3] = round(self.data_list[2] * 0.1)
    #     self.data_list[4] = self.data_list[2] + self.data_list[3]
    #     self.data_list[1] = round((self.data_list[5] / self.data_list[2]) * 100)
    
        
class MarginCalc():
    def __init__(self):

        self.data_list = []
        '''
        buy_cost = 0
        margin_rate = 1
        price = 2
        price_tax = 3
        price_wtax = 4
        margin = 5
        '''
    @property
    def priceList(self):
        return self.data_list

    @priceList.setter
    def priceList(self, set_data_list):
        self.data_list = set_data_list
        


    def calc_by_price(self):
        self.data_list[5] = self.data_list[2] - self.data_list[0]
        self.data_list[1] = round((self.data_list[5] / self.data_list[2]) * 100)
        self.data_list[3] = round(self.data_list[2] * 0.1)
        self.data_list[4] = self.data_list[2] + self.data_list[3]
    
    def calc_by_price_wtax(self):
        self.data_list[2] = round(self.data_list[4] / 1.1)
        self.data_list[5] =  self.data_list[2] - self.data_list[0]  
        self.data_list[1] = round((self.data_list[5] / self.data_list[2]) * 100)
        self.data_list[3] = round(self.data_list[2] * 0.1)
        
    def calc_by_margin_rate(self):
        self.data_list[2] = round(self.data_list[0] / (1-(self.data_list[1]/100)))
        self.data_list[5] =  self.data_list[2] - self.data_list[0]  
        self.data_list[3] = round(self.data_list[2] * 0.1)
        self.data_list[4] = self.data_list[2] + self.data_list[3]

    def calc_by_margin(self):
        self.data_list[2] = self.data_list[0] + self.data_list[5]
        self.data_list[3] = round(self.data_list[2] * 0.1)
        self.data_list[4] = self.data_list[2] + self.data_list[3]
        self.data_list[1] = round((self.data_list[5] / self.data_list[2]) * 100)
    
    def ddd(self):
        for i in self.data_list:
            print(type(i))
            
            
            
            

        
        
a = MatrixDataSet(10)  

a.addInitList()
a.addInitList()
a.addInitList()
a.addInitList()
# a.printList()
a.delData(1)
a.setData(0,1,100)        
a.setData(0,2,200)        
a.setData(0,3,300)        
a.setData(0,4,400)        
# a.print()  
# a.resetData(0)
print(a.getData[0])
a.addInitList()



        
    # @property
    # def priceList(self):
    #     return self.data_list

    # @priceList.setter
    # def priceList(self, set_data_list):
    #     self.data_list = set_data_list
        


    # def calc_by_price(self):
    #     self.data_list[5] = self.data_list[2] - self.data_list[0]
    #     self.data_list[1] = round((self.data_list[5] / self.data_list[2]) * 100)
    #     self.data_list[3] = round(self.data_list[2] * 0.1)
    #     self.data_list[4] = self.data_list[2] + self.data_list[3]
    
    # def calc_by_price_wtax(self):
    #     self.data_list[2] = round(self.data_list[4] / 1.1)
    #     self.data_list[5] =  self.data_list[2] - self.data_list[0]  
    #     self.data_list[1] = round((self.data_list[5] / self.data_list[2]) * 100)
    #     self.data_list[3] = round(self.data_list[2] * 0.1)
        
    # def calc_by_margin_rate(self):
    #     self.data_list[2] = round(self.data_list[0] / (1-(self.data_list[1]/100)))
    #     self.data_list[5] =  self.data_list[2] - self.data_list[0]  
    #     self.data_list[3] = round(self.data_list[2] * 0.1)
    #     self.data_list[4] = self.data_list[2] + self.data_list[3]

    # def calc_by_margin(self):
    #     self.data_list[2] = self.data_list[0] + self.data_list[5]
    #     self.data_list[3] = round(self.data_list[2] * 0.1)
    #     self.data_list[4] = self.data_list[2] + self.data_list[3]
    #     self.data_list[1] = round((self.data_list[5] / self.data_list[2]) * 100)
    
    # def ddd(self):
    #     for i in self.data_list:
    #         print(type(i))
            