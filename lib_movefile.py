import os
from pathlib import *
import directory_name 
import shutil

import glob
# DIRECTORY_PATH = './fax_receive/'

class MoveFile():
    
    def __init__(self, fax_path, selected_files, dst_root_path):
        
        self.FAX_DIR = fax_path
        self.DEST_ROOT_FOLDER = dst_root_path
        self.selected_files = selected_files

        self.files=[]
        
        self.invalid_datas = []
        self.vaild_datas = []
        
        self.dir_list = self.list_folders(dst_root_path)
        self._files_validation()

    def get_fileList(self):
        return self.vaild_datas , self.invalid_datas

    def list_folders(self, directory):
        contents = os.listdir(directory)
        folders = [content for content in contents if os.path.isdir(os.path.join(directory, content))]
        return folders

    def is_that_dir(self, dir):
        folders = [content for content in self.dir_list if dir in content]
        return folders

    def _files_validation(self) : 
        for file in self.selected_files:
            vaild_files = []
            invaild_files = []
            result_error = 0
            
            path_file = os.path.join(self.FAX_DIR, file)
            
            if os.path.isfile(path_file): # Source file validation
                vaild_files.append(path_file)
                
                key = self._get_key(file)
                toDir = self.is_that_dir(key)
                path_toDir = os.path.join(self.DEST_ROOT_FOLDER, toDir)
                if len(toDir) == 1:
                    vaild_files.append(path_toDir)
                    vaild_files.append(True)
                
                elif len(toDir) > 1 :
                    print(toDir)
                    
                elif not toDir :
                    invaild_files.append(path_file)
                    invaild_files.append(path_toDir)
                    result_error += 10
                    invaild_files.append(result_error)
                
            else :
                invaild_files.append(path_file)
                invaild_files.append(path_file)
                result_error = 100
                invaild_files.append(result_error)
            
            
            
                
           
        
        
                
            
            
            
            dst_path = os.path.join(self.DEST_ROOT_FOLDER, dir)
            if os.path.isdir(dst_path) :
                return dst_path
    
            
            
            dst_dir = self._validation_dst_directory(dir)
            result_file.append(dir)
            
            if dst_dir == 100:
                result_error += 'no dir'
            elif dst_dir == 200:
                result_error += 'new company'
            else :
                result_file[1] = dst_dir
   
            result_file.append(result_error)
            
            
            if result_file[2] =='':
                self.vaild_datas.append(result_file)
            else:
                self.invalid_datas.append(result_file)
                
            
            
            
                
                
    def _validation_src_file(self, file):
        
        path_file = os.path.join(self.FAX_DIR, file)
        if os.path.isfile(path_file): # Source file validation
            return path_file
        else :
            return 100
        
    def _validation_dst_directory(self, dir):
        
        
        if dir:
            dst_path = os.path.join(self.DEST_ROOT_FOLDER, dir)
            if os.path.isdir(dst_path) :
                return dst_path
            else :
                return 100
        else : 
            return 200
    
            
    def _get_key(self, path_file):
        # base_file = os.path.basename(path_file)
        start_index = 3 if path_file.startswith('[v]') is True else 0
        end_index = path_file.find('_')
        return path_file[start_index : end_index]
    
    
    

    def run(self):
        contents = glob.glob(self.src_path +'/*.*')
        files=[x for x in contents if not os.path.isdir(x)]
        
        if os.path.isfile(f'{self.src_path}/output.txt'):
            os.remove(f'{self.src_path}/output.txt')
        
        log_f = open(f"{self.src_path}/output.txt", "a")
        
        for f in files:
            log = self.__move_file(os.path.basename(f))
            print(log, file=log_f)
            
        log_f.close()
        

# mov = MoveFile('./fax_receive/','./fax_receive/')

# mov.run()
