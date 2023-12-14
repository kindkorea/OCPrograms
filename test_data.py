
import math

class MarginCalc():
    def __init__(self,buy_cost):
        self.data_list = ['매입가','공급가','마진율(%)','마진금','부가세','판매가']
        self.calc_data = {
            'buy_cost' : [ '매입가', 0],
            'margin_rate' : [ '공급가', 0],
            'price' : [ '마진율(%)', 0],
            'price_tax' : [ '마진금', 0],
            'price_wtax' : [ '부가세', 0],
            'margin' : [ '판매가', 0]
        }
        
        
        
        
    def reset(self):
        for ix in self.calc_data.values():
            print(ix)
        
    
    def calc_by_margin_rate(self,margin_rate):
        self.reset()
        self.margin_rate = margin_rate
        self.price = round(self.buy_cost / (1-(margin_rate/100)))
        self.price_tax = round(self.price * 0.1)
        self.price_wtax = self.price + self.price_tax
        self.margin = self.price - self.buy_cost
        
    def calc_by_margin(self,margin):
        self.reset()
        self.margin = margin
        self.price = round(self.buy_cost + self.margin)
        self.margin_rate = round((self.margin / self.price) * 100)
        self.price_tax = round(self.price * 0.1)
        self.price_wtax = self.price + self.price_tax
        
        
    def calc_by_price(self,price):
        self.reset()
        self.price = price
        self.margin =  self.price  - self.buy_cost
        self.margin_rate = round((self.margin / self.price) * 100)
        self.price_tax = round(self.price * 0.1)
        self.price_wtax = self.price + self.price_tax
        
    def marginCalc_print(self):
        print(f'{self.buy_cost=}')
        print(f'{self.margin_rate=}')
        print(f'{self.price=}')
        print(f'{self.price_tax=}')
        print(f'{self.price_wtax=}')
        print(f'{self.margin=}')
        print('')
        

app = MarginCalc(10000)
app.calc_by_margin_rate(20)
app.marginCalc_print()

app.calc_by_margin(2500)
app.marginCalc_print()

app.calc_by_price(12500)
app.marginCalc_print()