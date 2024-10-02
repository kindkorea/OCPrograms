from io import BytesIO
import PIL
from PIL import Image
import win32clipboard
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
        if os.path.isfile(selected_file):
            image = Image.open(selected_file)
            output = BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()    
            
        else : 
            print(f"There is no file")
            
    def _open_folder(self):
        os.startfile(self.PDF_TO_JPG_DST_PATH)
    
    def _most_recent_pdf( self):
        
        try :
            load_files = glob.glob(self.PDF_SRC_PATH+'/*.*')
            
            pdf_file_list = [file for file in load_files if file.endswith('.pdf' and '.PDF')] #pdf 파일 검출
            
            pdf_files_with_time =[]
            # print(pdf_file_list)
            for pdf_file in pdf_file_list:
                pdf_files_with_time.append((pdf_file,os.path.getctime(pdf_file)))
            return max(pdf_files_with_time,key=lambda x: x[1])[0]
        except : 
            print("_most_recent_pdf err was ocurred")
    
    def _cmd_createDirectory(self,directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print(f"Error: Failed to create the directory.{e}")

    def _pdf_to_jpg(self, src_file , dst_path , change_filename):
        
        try : 
            pages = convert_from_path(src_file, dpi=200, poppler_path='./poppler-23.11.0/Library/bin')
            output_filelist = []              
            file_path = f'{dst_path}/{change_filename}'
     
            self._cmd_createDirectory(file_path)
            os.startfile(file_path)

            for i, page in enumerate(pages):
                o_filename = f"{file_path}/{change_filename}#{str(i)}.jpg" 
                page.save(o_filename, "JPEG")
                output_filelist.append(o_filename)

            return  output_filelist
        except Exception as e:
            print(f"__pdf_to_jpg : {e}")

   
    def _cmd_re_name(self,src_file, dest_path, change_filename):
        
        file_name_ext = os.path.basename(src_file)
        _ , file_ext = os.path.splitext(file_name_ext)
        file_path = f'{dest_path}/{change_filename}'
        rename = f'{file_path}/{change_filename}{file_ext}'
        
        self._cmd_createDirectory(file_path)
        os.startfile(file_path)
        
        if os.path.exists(rename):
            print(f"{rename} is exist")
        else :    
            os.rename(src_file , rename)
            return rename    



    def cmd_pdf_to_jpg(self,filename):

        pdfFile = self._most_recent_pdf()

        if not pdfFile :
            print('no pdf file')
        else :
            self.converted_jpg_filelist = self._pdf_to_jpg(pdfFile , self.PDF_TO_JPG_DST_PATH,  filename)
        
    def get_converted_count(self):
        if self.converted_jpg_filelist :
            return len(self.converted_jpg_filelist)
        else :
            return False

    def cmd_rename(self, filename):
      
        pdfFile = self._most_recent_pdf()     
        self._cmd_re_name(pdfFile, self.PDF_TO_JPG_DST_PATH, filename)
       

        