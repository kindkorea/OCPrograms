
import datetime
from io import BytesIO
from PIL import Image
import win32clipboard
# import time 
import os

from pdf2image import convert_from_path

import glob 

class P2J():
    def __init__(self, src_path, dst_path):

        self.PDF_SRC_PATH = src_path
        self.PDF_TO_JPG_DST_PATH = dst_path
        self.coverted_jpg_count = 0
        self.converted_jpg_filelist = []
        # self.bnt_list_cb = []

    def send_to_clipboard(self,index):
        
        selected_file = self.converted_jpg_filelist[index]
        if selected_file is None:
            print(f"There is no file")
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
            

    def __most_recent_pdf( self):
        load_files = glob.glob(self.PDF_SRC_PATH+'/*.*')
        pdf_file_list = [file for file in load_files if file.endswith('.pdf' and '.PDF')]
        pdf_files_with_time =[]
        # print(pdf_file_list)
        for pdf_file in pdf_file_list:
            pdf_files_with_time.append((pdf_file,os.path.getctime(pdf_file)))
        return max(pdf_files_with_time,key=lambda x: x[1])[0]
    
    def __cmd_createDirectory(self,directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print(f"Error: Failed to create the directory.{e}")

    def __pdf_to_jpg(self, src_file , dst_path , change_filename):
        
        try : 
            pages = convert_from_path(src_file, dpi=200, poppler_path='./poppler-23.11.0/Library/bin')
            output_filelist = []              
            file_path = f'{dst_path}/{change_filename}'
     
            self.__cmd_createDirectory(file_path)
            # print(file_path)
            os.startfile(file_path)

            for i, page in enumerate(pages):
                o_filename = f"{file_path}/{change_filename}#{str(i)}.jpg" 
                page.save(o_filename, "JPEG")
                output_filelist.append(o_filename)

            return  output_filelist
        except Exception as e:
            print(f"__pdf_ti_jpg : {e}")

   
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



    def cmd_pdf_to_jpg(self,filename):

        recent_pdf = self.__most_recent_pdf()

        if not recent_pdf :
            print('no pdf file')
        else :
            self.converted_jpg_filelist = self.__pdf_to_jpg(recent_pdf , self.PDF_TO_JPG_DST_PATH,  filename)
        
    def get_converted_count(self):
        if self.converted_jpg_filelist is not None:
            return len(self.converted_jpg_filelist)

    def cmd_rename(self, filename):
      
        recent_pdf = self.__most_recent_pdf()     
        self.__cmd_re_name(recent_pdf, self.PDF_TO_JPG_DST_PATH, filename)
       

        