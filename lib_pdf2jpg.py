from io import BytesIO
import PIL
from PIL import Image
import win32clipboard
import os
from ConfigControlFile import ConfigureIni


from pdf2image import convert_from_path

import glob 
import time
from datetime import datetime

class P2J():
    def __init__(self):

        self.PDF_SRC_PATH = ConfigureIni.read('pdf parser','from_pdf_folder')
        self.PDF_TO_JPG_DST_PATH = ConfigureIni.read('pdf parser','save_folder')
        self.coverted_jpg_count = 0
        self.converted_jpg_filelist = []
        self.selected_pdf = ''

    @property
    def pdf(self):
        return self.selected_pdf
    
    
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
    
    def _most_recent_pdf2( self):
        current_time = time.time()
        try :
            load_files = glob.glob(self.PDF_SRC_PATH+'/*.*')
            
            pdf_file_list = [file for file in load_files if file.endswith('.pdf' and '.PDF')] #pdf 파일 검출
            
            pdf_files_with_time =[]
            # print(pdf_file_list)
            for pdf_file in pdf_file_list:
                pdf_files_with_time.append((pdf_file, os.path.getctime(pdf_file)))
            
            lately_pdf = max(pdf_files_with_time,key=lambda x: x[1])[0]
            modification_time = os.path.getmtime(lately_pdf)
            # print(f'{current_time - modification_time=}')
            if current_time - modification_time < 60000 :
                self.selected_pdf = lately_pdf + "  " + datetime.fromtimestamp(modification_time).strftime('%H:%M:%S')
                return lately_pdf
            else : 
                return False
        except : 
            print("_most_recent_pdf err was ocurred")
            
    def _most_recent_pdf(self):
        current_time = time.time()
        try :
            load_files = glob.glob(self.PDF_SRC_PATH+'/*.*')
            pdf_file_list = [file for file in load_files if file.endswith('.pdf' and '.PDF')] #pdf 파일 검출
        
            if pdf_file_list:
                latest_file = max(pdf_file_list, key=os.path.getmtime)
                modification_time = os.path.getmtime(latest_file)
                if current_time - modification_time < 1800 :  #30분 이내 파이말 유효함
                    self.selected_pdf = latest_file + "  " + datetime.fromtimestamp(modification_time).strftime('%H:%M:%S')
                    print(self.selected_pdf)
                    return latest_file
        
            return False
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
            os.remove(src_file)
            return  output_filelist
        
        except Exception as e:
            print(f"__pdf_to_jpg : {e} src ={src_file}")

   
    def _cmd_re_name(self,src_file, dest_path, change_filename):
        
        file_name_ext = os.path.basename(src_file)
        _ , file_ext = os.path.splitext(file_name_ext)
        file_path = f'{dest_path}/{change_filename}'
        rename = f'{file_path}/{change_filename}{file_ext}'
        
        self._cmd_createDirectory(file_path)
        os.startfile(file_path)
        os.rename(src_file , rename)
        


    def cmd_pdf_to_jpg(self,filename):

        src_pdf_file = self._most_recent_pdf()
        if src_pdf_file :
            self.converted_jpg_filelist = self._pdf_to_jpg(src_pdf_file , self.PDF_TO_JPG_DST_PATH,  filename)
            return self.converted_jpg_filelist
        else :
            return False
        
    def get_converted_count(self):
        if self.converted_jpg_filelist :
            return len(self.converted_jpg_filelist)
        else :
            return False

    def cmd_rename(self, filename):
      
        pdfFile = self._most_recent_pdf()     
        if pdfFile :
            self._cmd_re_name(pdfFile, self.PDF_TO_JPG_DST_PATH, filename)
            return pdfFile
            # pass
        else : 
            False
            

        