import math

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
            
