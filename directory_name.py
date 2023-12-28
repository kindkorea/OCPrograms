import os

import tkinter as tk
from tkinter import ttk
from tkinter import * # __all__
import lib_movefile
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
class FileMove:
    def __init__(self, master, src_files, src_path, dst_dir):
        
        self.main_data = CompanyList.keys()
        # self.src_files = src_files
        
        self.master = master
        self.master_position_X = self.master.winfo_rootx()
        self.master_position_Y = self.master.winfo_rooty()
        
        self.popup_window = Toplevel(master)
        self.popup_window.title("Move file Window")
        self.popup_window.geometry(f'200x300+{self.master_position_X}+{self.master_position_Y+300}')
        
        self.move_file = lib_movefile.MoveFile( src_path , src_files, dst_dir)
        
        self.valid_datas, self.invalid_datas = self.move_file.get_fileList()

        self.create_widgets()
        
    def create_widgets(self):
        self.mid_frame = Frame(self.popup_window)
        self.mid_frame.grid(row=1,column=0) 

        all_data = self.valid_datas + self.invalid_datas
        for ix , file in enumerate(all_data):
            
            if file[2] == '':
                self.create_rowLine(self.mid_frame, ix, file[0],file[1],'가능함')
            else :
                self.create_rowLine(self.mid_frame, ix, file[0],file[1],file[2])
                
        
        self.bottomFrame = Frame(self.popup_window )
        self.bottomFrame.grid(row=2,column=0) 
        Button(self.bottomFrame, text = '확인').grid(row=0, column=0)
        Button(self.bottomFrame, text = '취소', command=self.popup_window.destroy).grid(row=0, column=1)


    def create_rowLine(self,container, row, src_file, dest_dir, result):
        Label(container,  text=src_file, justify="left").grid(row=row, column=0)
        Label(container, text=f'→   {dest_dir} :', justify="left" ).grid(row=row, column=1)
        Label(container, text=result).grid(row=row, column=2)
        
        

class CompanyListWidget:
    def __init__(self, master, handler):
        
        self.main_data  =  CompanyList.keys()
        self.select_handler = handler
        
        
        self.master = master
        self.master_position_X = self.master.winfo_rootx()
        self.master_position_Y = self.master.winfo_rooty()
        
        
        self.popup_window = Toplevel(master)
        self.popup_window.title("Popup Window")
        self.popup_window.geometry(f'200x300+{self.master_position_X}+{self.master_position_Y+300}')
        self.selected_item = StringVar()
        self.search_str = StringVar()
        
        self.search = Entry(self.popup_window, textvariable=self.search_str )
        self.search.grid(row=0,column=0,pady=10)
        self.search.focus()
        self.search.bind('<Key>', self._handler_key)
        # self.search.bind("<KeyPress>", self.cb_search)
     
        self.listbox = Listbox(self.popup_window, selectmode = 'single')
        self.listbox.bind('<<ListboxSelect>>', self._handlerList)
        self.listbox.bind('<Double-Button-1>', self._handlerList)
        self.listbox.grid(row=1,column=0)
        
        self.scrollbar=Scrollbar(self.popup_window, orient='vertical' ,command=self.listbox.yview)
        self.scrollbar.grid(row=1, sticky='nse')
        
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        
        
        
        self.fill_listbox(self.main_data)

    def _handlerList(self, e):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_value = self.listbox.get(selected_index[0])
            self.select_handler(selected_value)
            self.popup_window.destroy()
            
            
    # def __handler_listbox_double_click(self, e):
    #     self.select_handler(self.selected_item)
    
    def _handler_key(self,e):
        key = e.keycode
        print(key)
        
        if key == 40 or key == 38 : # arrow up down
            self.listbox.focus()
        # elif key == 13 or key == 32 : # enter and space
        
        self.cb_search()
        
    def search_korean_list(self, search_term, korean_list):
        if search_term in korean_list:
            return search_term
   
    def cb_search(self):
        sstr = self.search_str.get()
        
        filtered_data = []
        if sstr == "":
            self.fill_listbox(self.main_data)
            return
        
        for item in self.main_data:
            if sstr in item:
                filtered_data.append(item)
                
        if not filtered_data:
            return    
        self.fill_listbox(filtered_data) 
        
    
    def fill_listbox(self, ld):
        self.listbox.delete(0, END)
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
        # c_list = CompanyList.keys()
        c_list = ['sadfasdf', '[v]형제철물_2023-12-08.jpg','[v]호성주유소_20231201_151702.jpg']
        fax_receive = FileMove(self ,c_list,'./fax_receive','./fax_receive')
        
    def handler(self,f_name):
        print(f'evnet {f_name}')

        
if __name__ == "__main__":
    app = App()
    app.mainloop()        
    