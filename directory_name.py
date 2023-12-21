import os

import tkinter as tk
from tkinter import ttk
from tkinter import * # __all__

# import directory_name

# PATH = 'C:/Users/kindk/OneDrive/OCWOOD_OFFICE/002_매입처/01_수신팩스/'
# KEY_FILENAME = 0
# KEY_FORDER = 1


CompanyList = {
    '경비':        '경비',
    '기타':        '기타',
    '건한':        '건한_철물',
    '구산목재':    '구산목재_목재',
    '남창':        '남창_목재',
    '다인디앤씨':  '다인디앤씨(오일스테인)철물',
    '대한테이프':  '대한테이프_철물',
    '대현우드':    '대현우드_목재',
    '두산종합목재':'두산종합목재',
    '락소':        '락소_히든몰딩_몰딩',
    '마운틴우드':  '마운틴우드_목재',
    '미래상사':    '미래상사_몰딩',
    '방음랜드':    '방음랜드_흡음재',
    '벽산':        '벽산_단열재',
    '벽산인슈-예스건축자재':'벽산인슈:예스건축자재_단열재',
    '복음단열':    '복음단열_단열재',
    '삼원목재':    '삼원목재_합판',
    '에스디팀버':  '에스디팀버_목재',
    '예성템바':    '예성템바_몰딩',
    '오스방음':    '오스방음_흡음재',
    '우드마트':    '우드마트_목재',
    '우진프레임':  '우진프레임_몰딩',
    '케이디우드':  '케이디우드_합판',
    '케이론몰딩':  '케이론몰딩_몰딩',
    '케이씨씨':    '케이씨씨_석고',
    '크나우프':    '크나우프_석고',
    '태신합판':    '태신합판_합판',
    '태진목재':    '태진목재_목재',
    '팀버마스타':  '팀버마스타_목재',
    '하이우드':    '하이우드_몰딩',
    '한국스츠로폼':'한국스츠로폼_단열재',
    '한성우드':    '한성우드_목재',
    '형제철물':    '형제철물_철물',
    '홍진테크':    '홍진테크_흡음재',
}

class CompanyListWidget(Frame):
    def __init__(self,container, name_list, eventHandler):
        super().__init__(container)
        
        self.main_data  = name_list
        # self.src_path = src_path
        # self.dst_path = dst_path
        
        self.select_handler = eventHandler
        
        self.selected_item = StringVar()
        
        self.search_str = StringVar()
        
        self.search = Entry(self, textvariable=self.search_str )
        self.search.grid(row=0,column=0,pady=10)
        self.search.bind('<Key>', self.handler_key)
        
     
        self.listbox = Listbox(self, selectmode = 'single')
        self.listbox.bind('<<ListboxSelect>>', self.__handlerList)
        self.listbox.bind('<Double-Button-1>', self.__handler_listbox_double_click)
        self.listbox.grid(row=1,column=0)
        
        self.scrollbar=Scrollbar(self, orient='vertical' ,command=self.listbox.yview)
        self.scrollbar.grid(row=1, sticky='nse')
        
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        
        
        
        self.fill_listbox(self.main_data)
        
    @property
    def getName(self):
        return self.selected_item 
    
    @getName.setter
    def getName(self):
        pass
        
    def __handlerList(self, e):
        
        # print('handlerList in  CompanyListWidget class')
        selected_tuple = self.listbox.curselection()
        if not selected_tuple:
            return 
        index =  selected_tuple[0]
        # print(f'__selected_src_file={index=}')
        if index is not None: # if the tuple is not empty
            self.search.delete(0,END)
            self.search.insert(0,self.listbox.get(index))
            self.select_handler(self.selected_item)
            self.selected_item = self.search.get()
            
            # self.select_handler(self.search.get())
    def __handler_listbox_double_click(self, e):
        self.select_handler(self.selected_item)
    
    def handler_key(self,e):
        key = e.keycode
        print(key)
        
        if key == 40 or key == 38 : # arrow up down
            self.listbox.focus()
        elif key == 13 or key == 32 : # enter and space
            self.cb_search()
        
        
    def cb_search(self):
        sstr = self.search_str.get()
        self.listbox.delete(0, END)
        # If filter removed show all data
        if sstr == "":
            self.fill_listbox(self.main_data) 
            return
    
        filtered_data = list()
        for item in self.main_data:
            if item.find(sstr) >= 0:
                filtered_data.append(item)
    
        self.fill_listbox(filtered_data)   
    
    def fill_listbox(self, ld):
        for item in ld:
            self.listbox.insert(END, item)
    
    def get_filename(self):
        return self.search.get()
  
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
        c_list = CompanyList.keys()
        
        # print(key)
        fax_receive = CompanyListWidget(self, c_list ,self.handler)
        fax_receive.grid(column=0, row=1)
        # # create the button frame
        # button_frame = gui_pdf2jpg.Cb_Btn_frame(self,8)
        
    def handler(self,f_name):
        print('evnet {f_name}')

        
if __name__ == "__main__":
    app = App()
    app.mainloop()        
    