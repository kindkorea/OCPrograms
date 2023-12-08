import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import * # __all__
import datetime
from io import BytesIO
from PIL import Image
import win32clipboard
# import time 
import os

from pdf2image import convert_from_path

import glob 


class PDFconvert(LabelFrame):

    def __init__(self, master, src_path, dst_path):
        super().__init__(master)
        self.NUMBER_OF_CB = 8
        self.PDF_SRC_PATH = src_path
        self.PDF_TO_JPG_DST_PATH = dst_path
        
        # self.src_file =''
        self.converted_jpg = []
        self.bnt_list_cb = []

        self.initialize()
        # self.master[LabelFrame]['text'] = 'hello'

    # setting GUI
    def initialize(self):

        self.frame_run = LabelFrame(self,text='button')
        self.btn_convert_jpg = Button(self.frame_run, padx=5, pady=5, text="JPG변환", width=12, command=self.cmd_pdf_to_jpg)
        self.btn_convert_jpg.pack(side="right", padx=5, pady=5)

        self.btn_rename = Button(self.frame_run, padx=5, pady=5, text="이름변경", width=12, command=self.cmd_rename)
        self.btn_rename.pack(side="right", padx=5, pady=5)

        self.month = datetime.datetime.now().month
        self.make_mid_content = Entry(self.frame_run)
        self.make_mid_content.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) # 높이 변경
        self.make_mid_content.insert(END,f"{self.month}월 청구서")

        self.make_comp_name = Entry(self.frame_run)
        self.make_comp_name.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) # 높이 변경
        self.make_comp_name.insert(END,f"업체명")
        self.frame_run.pack(fill="x", padx=5, pady=5)

        
        # copy to clipboard button
        self.frame_cb = LabelFrame(self, text="Copy to Clipboard")
    
        for i in  range(self.NUMBER_OF_CB):
            self.bnt_list_cb.append(self.__make_btn(self.frame_cb, 1, i, 6, f'CB{i+1}'))
            
        self.frame_cb.pack(fill="x", padx=5, pady=5, ipady=5)

    def __btn_cell_data(self, index):
        self.__send_to_clipboard(index)
        print(index)

    def __make_btn(self,frame, row, column, width, text):
        e = Button(frame, width=width , text = text , command= lambda : self.__btn_cell_data(column))
        e.coords = (row-1, column-1)
        e.grid(row=row, column=column)
        return e
    
    def __btn_color(self,index,state):
        self.bnt_list_cb[index].configure(bg=state)

    
    def __send_to_clipboard(self,index):
        
        selected_file = self.converted_jpg[index]
        if not selected_file:
            self.cb_label.set(f"There is no file")
        else : 
            # file_name = os.path.basename(selected_file)
            image = Image.open(selected_file)
            output = BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()    
            self.__btn_color(index,'#f0f0f0')

    def __most_recent_pdf( self):
        load_files = glob.glob(self.PDF_SRC_PATH+'/*.*')
        pdf_file_list = [file for file in load_files if file.endswith('.pdf' and '.PDF')]
        pdf_files_with_time =[]
        print(pdf_file_list)
        for pdf_file in pdf_file_list:
            pdf_files_with_time.append((pdf_file,os.path.getctime(pdf_file)))
        return max(pdf_files_with_time,key=lambda x: x[1])[0]
    
    def __cmd_createDirectory(self,directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("Error: Failed to create the directory.")

    def __pdf_to_jpg(self, src_file , dst_path , change_filename):
        
        try : 
            # most_recent_pdf = self.__most_recent_pdf()
            print(src_file)
            pages = convert_from_path(src_file, dpi=200)
            print(pages)
            output_filelist = []  
            file_path = f'{dst_path}/{change_filename}'

            self.__cmd_createDirectory(file_path)
            os.startfile(file_path)

            for i, page in enumerate(pages):
                o_filename = f"{file_path}/{change_filename}#{str(i)}.jpg" 
                page.save(o_filename, "JPEG")
                output_filelist.append(o_filename)

            return  output_filelist
        except :
            print("No PDF file.")

   


    def cmd_pdf_to_jpg(self):

        recent_pdf = self.__most_recent_pdf()

        if not recent_pdf :
            print('no pdf file')
        else :
            f_name = f'웅천목재_{self.make_mid_content.get()}_{self.make_comp_name.get()}'
            self.converted_jpg = self.__pdf_to_jpg(recent_pdf , self.PDF_TO_JPG_DST_PATH,  f_name)

            for i in range(self.NUMBER_OF_CB):
                if len(self.converted_jpg) <= i :
                    self.__btn_color(i,'#f0f0f0')
                  
                else : 
                    self.__btn_color(i,'red')

    def __cmd_re_name(self,src_file, dest_path, change_filename):
        
        file_name_ext = os.path.basename(src_file)
        file_name, file_ext = os.path.splitext(file_name_ext)
        file_path = f'{dest_path}/{change_filename}'
        rename = f'{file_path}/{change_filename}{file_ext}'
        
        self.__cmd_createDirectory(file_path)
        os.startfile(file_path)
        if os.path.exists(rename):
            print(f"{rename} is exist")
        else :    
            os.rename(src_file , rename)
            return rename    

    def cmd_rename(self):
        if self.make_comp_name.get() != '업체명' :
            recent_pdf = self.__most_recent_pdf()

            f_name = f'웅천목재_{self.make_mid_content.get()}_{self.make_comp_name.get()}'
            # result = pdf_file.pdf_rename(txt_dest_path.get(),f_name)

            if not self.__cmd_re_name(recent_pdf, self.PDF_TO_JPG_DST_PATH, f_name) :
                msgbox.showwarning('경고','PDF 파일이 없습니다.')

            self.make_comp_name.delete(0,'end')
            self.make_comp_name.insert(END,"업체명")

        else :
            # print("업체명을 입력하세요.")
            msgbox.showwarning('경고','업체명을 입력하세요')

    

    

