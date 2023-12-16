import os
import glob
import time
import sys
import subprocess


class FaxReceive():
    def __init__(self, fax_path):
        
        # self.DIRECTOR_PATH = dir_path
        self.__selected_file =''
        # self.src_path = self.DIRECTOR_PATH
        self.EXTENTION_VIEWER = 'c:/Users/kindk/AppData/Local/Imagine/Imagine64.exe'
        # self.FAX_DIRECTOR_PATH = 'C:/Users/kindk/OneDrive/OCWOOD_OFFICE/FAX_received/'
        self.FAX_DIRECTOR_PATH = fax_path 
        
    @property
    def selectitem(self):
        return self.__selected_file
    
    @selectitem.setter
    def selectitem(self, file):
        self.__selected_file = file

    @property
    def selectedfile(self):
        return f'{self.FAX_DIRECTOR_PATH}{self.selectitem}'
    

        
    def __get_directory_file(self):
        return  glob.glob(self.FAX_DIRECTOR_PATH +'/*.*')
        # return  [file for file in load_files if file.endswith('.jpg')]
    
    def __get_sorted_faxfiles(self,file_list):
        checked_list = []
        unchecked_list = [] 
        
        file_list.sort(key=os.path.getmtime)

        for f in file_list:
            if os.path.basename(f)[1] == 'v':
                checked_list.append(f)
            else :
                unchecked_list.append(f)
        return unchecked_list, checked_list
    
    def get_faxfiles(self):
        return self.__get_sorted_faxfiles(self.__get_directory_file())     
    
    
    def Rename_file(self, dst_name):
        if os.path.isfile(self.selectedfile):
            file_ext = os.path.splitext(self.selectedfile)[1] 
            file_ctime = time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(self.selectedfile)))
            dst_file_name = f'{self.FAX_DIRECTOR_PATH}{dst_name}_{file_ctime}{file_ext}'
            # print(f'src_file : {src_file}')
            # print(f'dst_file : {dst_file_name}')
            os.rename(self.selectedfile, dst_file_name)
                    
        else :
            print(f'Rename_file error : {dst_name} is not found')
    
    def Checking_file(self):
        if os.path.isfile(self.selectedfile):
            f_name = os.path.basename(self.selectedfile)
            # print(f'Checking_file {f_name=}')
            
            if f_name[1] == 'v':
                d_name = f_name.split('[v]')
                dst_file_name = f'{self.FAX_DIRECTOR_PATH}{d_name[1]}'
            else :
                dst_file_name = f'{self.FAX_DIRECTOR_PATH}[v]{f_name}'
            print(f'Checking_file src_file : {self.selectedfile}')
            print(f'Checking_file dst_file : {dst_file_name}')
            os.rename(self.selectedfile, dst_file_name)
                    
        else :
            print(f'Rename_file error : {src_file} is not found')
    
    def Delete_file(self):
        print(f'Delete_file={self.selectedfile}')
        
        if os.path.isfile(self.selectedfile):
            os.remove(self.selectedfile)
        else : 
            print(f"Delete_file error : {self.selectedfile} is not found")
        
    def Run_with_viewer(self):
        cmd = f'{self.EXTENTION_VIEWER} {self.selectedfile}'
        print(f'__run_with_viewer = {cmd}')
        subprocess.Popen(cmd)
        
    
        
            