import os
import glob
import time
import sys
import subprocess


class FaxReceive():
    def __init__(self,file_path):
        
        self.EXTENTION_VIEWER = 'c:/Users/kindk/AppData/Local/Imagine/Imagine64.exe'
        self.FAX_DIRECTOR_PATH = file_path
        # self.samefile_index = 0
    def get_faxfiles(self):
        return self._get_sorted_faxfiles(self._get_files_inDirectory())     
    
    
    def rename_to_company(self, src_file ,dst_name):
        
        # samefile_index =0
        src_path_file = os.path.join(self.FAX_DIRECTOR_PATH,src_file)
        if os.path.isfile(src_path_file):
            try : 
                file_ext = os.path.splitext(src_file)[1] 
                file_ctime = time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(src_path_file)))
                dst_file_name = os.path.join(self.FAX_DIRECTOR_PATH, f'{dst_name}_{file_ctime}{file_ext}')
                
                for i in range(1,20):
                    if os.path.isfile(dst_file_name):
                        dst_file_name = os.path.join(self.FAX_DIRECTOR_PATH, f'{dst_name}_{file_ctime}_#{i}{file_ext}')
                    else :
                        break
                os.rename(src_path_file, dst_file_name)
                
            except FileExistsError :
                print(f'Error: The file {dst_file_name} exist.')
        else :
                print(f'Error: The file {src_path_file} does not exist.')
    
    def is_checked(self, src_file):
        src_file_path = os.path.join(self.FAX_DIRECTOR_PATH,src_file) 
        try : 
            if src_file[1] == 'v':
                d_name = src_file.split('[v]')[1]
                dst_file_name = os.path.join(self.FAX_DIRECTOR_PATH,d_name) 
            else :
                dst_file_name = os.path.join(self.FAX_DIRECTOR_PATH,f'[v]{src_file}') 
            os.rename(src_file_path, dst_file_name)
            
        except FileNotFoundError :
            print(f'Error: The file {src_file} does not exist.')
            
        except FileExistsError :
            print(f'Error: The file {dst_file_name} does not exist.')
    
    def delete_file(self,src_file):
        try : 
            os.remove(os.path.join(self.FAX_DIRECTOR_PATH,src_file))
            
        except FileNotFoundError :
            print(f'Error: The file {src_file} does not exist.')
                
    def run_with_viewer(self,src_file):
        
        try : 
            file_path = os.path.join(self.FAX_DIRECTOR_PATH,src_file)
            
            cmd = f'{self.EXTENTION_VIEWER} {file_path}'
            subprocess.Popen(cmd)
        
        except FileNotFoundError :
            print(f'Error: The file {src_file} does not exist.')
        
    def _get_files_inDirectory(self):
        try : 
            os.path.isdir(self.FAX_DIRECTOR_PATH)
            return os.listdir(self.FAX_DIRECTOR_PATH)
            
        except FileNotFoundError:
            print(f"Error: The directory '{self.FAX_DIRECTOR_PATH}' does not exist.")
            
    def _get_sorted_faxfiles(self,file_list):
        checked_list = []
        unchecked_list = [] 
        
        file_list.sort(key=lambda x: os.path.getmtime(os.path.join(self.FAX_DIRECTOR_PATH, x)))

        for f in file_list:
            if f[1] == 'v':
                checked_list.append(f)
            else :
                unchecked_list.append(f)
        return unchecked_list, checked_list

