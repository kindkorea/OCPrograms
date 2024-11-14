import os
import glob
import time
import sys
import subprocess
import shutil


        
class FaxReceive():
    def __init__(self, fax_folder_path):
        
        self.EXTENTION_VIEWER = 'c:/Users/kindk/AppData/Local/Imagine/Imagine64.exe'
        self.FAX_DIRECTOR_PATH = fax_folder_path
        
    def get_file_from_folder(self, folder_path):
        return self._get_sorted_faxfiles(self._get_files_inDirectory(folder_path))     
    
    
    def rename_to_company(self, src_file ,dst_name):
        
        src_path_file = os.path.join(self.FAX_DIRECTOR_PATH,src_file)
        if os.path.isfile(src_path_file):
            try : 
                file_stat = os.stat(src_path_file)
                created_timestamp = file_stat.st_ctime
                file_ctime = time.strftime('%Y-%m-%d', time.localtime(created_timestamp))

                file_ext = os.path.splitext(src_file)[1] 
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
            src_file_path = os.path.join(self.FAX_DIRECTOR_PATH,src_file)
            if os.path.isfile(src_file_path):
                try : 
                    # send2trash.send2trash(src_file_path)
                    shutil.move(src_file_path, f'{self.FAX_DIRECTOR_PATH}/../FAX_trashBin')
                except Exception as err :
                    print(f'send2trash occur exception {err}')
        except FileNotFoundError :
            print(f'Error: The file {src_file} does not exist.')
            
    def run_with_viewer(self,src_file):
        
        try : 
            file_path = os.path.join(self.FAX_DIRECTOR_PATH,src_file)
            
            cmd = f'{self.EXTENTION_VIEWER} {file_path}'
            subprocess.Popen(cmd)
        
        except FileNotFoundError :
            print(f'Error: The file {src_file} does not exist.')
    
    def _get_files_inDirectory(self,file_path):
        try : 
                # 폴더 내 모든 파일의 경로 가져오기
            files = [os.path.join(file_path, file) for file in os.listdir(file_path)]
            # 파일만 필터링하고 수정 시간 기준으로 정렬
            files = [file for file in files if os.path.isfile(file)]
            files.sort(key=os.path.getmtime )  # 수정 시간 기준으로 정렬
            return files
        except :
            print(f"Error: The directory '{self.FAX_DIRECTOR_PATH}' does not exist.")
            
    def _get_sorted_faxfiles(self,file_list):
        checked_list = []
        unchecked_list = [] 

        for f in file_list:
            if f[1] == 'v':
                checked_list.append(f)
            else :
                unchecked_list.append(f)
        return unchecked_list, checked_list

