import tkinter as tk
from tkinter import ttk
from tkinter import * # __all__
import lib_pdf2jpg
from tkinter import simpledialog
import os
import datetime
from io import BytesIO
import win32clipboard


class Pdf2jpg(Frame):
    def __init__(self, container):
        super().__init__(container)
        # setup the grid layout manager
        
        self.container = self
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(0, weight=3)
        
        self.cb_btns = 10
        self.cb_btn_list = []
        
        PDF_SRC_DIR_PATH = 'C:/Users/kindk/Downloads'
        PDF_TO_JPG_DEST_DIR_PATH = 'C:/Users/kindk/bills'

        self.P2J = lib_pdf2jpg.P2J(PDF_SRC_DIR_PATH,PDF_TO_JPG_DEST_DIR_PATH)
        # self.title_first  = StringVar()
        
        self._create_widgets()
        
        
        
    def _create_widgets(self):
        # Find what

        self.top_frame = LabelFrame(self.container,text='PDF파일을 이미지로 변환함 ')
        self.top_frame.grid(row=0, column=0 , padx=10 ,sticky='we')
        
        self.top_innerframe = Frame(self.top_frame)
        self.top_innerframe.grid(row=0, column=0 , padx=10 ,sticky='we')
        
        self.title_first = f'웅천목재_{datetime.datetime.now().month}월_청구서'
        self.entry_name_first = Entry(self.top_innerframe, width=15 , textvariable=self.title_first )
        self.entry_name_first.grid(column=0, row=0, padx= 5, sticky='w' )
        self.entry_name_first.insert(END,self.title_first)

        self.entry_name_second =Entry(self.top_innerframe, width=20)
        self.entry_name_second.grid(column=2, row=0, padx= 5, sticky='w')
  
        
        Button(self.top_innerframe, text='JPG변환', command=self._btn_pdf2jpg).grid(column=4, row=0,  padx= 5, pady= 5,sticky=tk.E )
        Button(self.top_innerframe, text='이름 변환', command=self._btn_rename).grid(column=6, row=0, padx= 5, pady= 5, sticky=tk.E)
        Button(self.top_innerframe, text='폴더 열기', command=self.P2J._open_folder).grid(column=7, row=0, padx= 5, pady= 5, sticky=tk.E)
        
        self.btn_f = Frame(self.top_frame)
        self.btn_f.grid(row=1,column=0)
        for i in range(self.cb_btns):
            self.cb_btn_list.append(self._make_btn(self.btn_f, 1, i , 5, f'CB_{i+1}'))

        for widget in self.winfo_children():
            widget.grid(padx=1, pady=3)
            
    def _popup_asking_filename(self):
        # the input dialog
        USER_INP = simpledialog.askstring(title="이름",
                                    prompt="이름을 입력하시오?")
         # check it out
        return USER_INP
    
    def _make_btn(self,frame, row, column, width, text):
        e = Button(frame, width=width , text = text , command= lambda : self._btn_cell_data(column))
        e.coords = (row-1, column-1)
        e.grid(row=row, column=column , padx=1)
        return e
    
    def _btn_cell_data(self,index):
        # print(f'__btn_cell_data = {index}')
        if index < self.P2J.get_converted_count():
            self.P2J.send_to_clipboard( index ) 
            # change button color 
            self._btn_color(index, '#f0f0f0')
        
        
    def _btn_color(self, index , state):
        self.cb_btn_list[index].configure(bg=state)
        # print(self.cb_btn_list[index])

    def _get_filename(self):
        
        title_sec = self.entry_name_second.get()
        if title_sec == '' or title_sec == None:
            title_sec = self._popup_asking_filename()
            # title_sec =  datetime.datetime.now().strftime('%Hh%Mm')
        return  self.entry_name_first.get() + '_'+ title_sec
    
    def _read_toCB(self, converted_count):
        
        for idx in range(self.cb_btns):
            self._btn_color(idx, '#f0f0f0' if idx >=  converted_count else 'red')
        
    def _btn_pdf2jpg(self):
        self.P2J.cmd_pdf_to_jpg(self._get_filename())
        self._read_toCB(self.P2J.get_converted_count())
        
    def _btn_rename(self):    
        self.P2J.cmd_rename(self._get_filename())
        self.entry_name_second.delete(END)

    def _clear_cb(self):
        self._read_toCB(0)

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
        fax_receive = Pdf2jpg(self)
        fax_receive.grid(column=0, row=1)
        # # create the button frame
        # button_frame = gui_pdf2jpg.Cb_Btn_frame(self,8)

        
if __name__ == "__main__":
    app = App()
    app.mainloop()        