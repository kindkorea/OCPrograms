import os
from pathlib import *
import directory_name 
import shutil

import glob
# DIRECTORY_PATH = './fax_receive/'

class MoveFile():
    
    def __init__(self, src_path, dst_root_path):
        
        self.src_path = src_path
        self.dst_root_path = dst_root_path
        # contents = glob.glob(self.src_path +'/*.*')
        self.files=[]

    

    def __get_key(self, path_file):
        # base_file = os.path.basename(path_file)
        start_index = 3 if path_file.startswith('[v]') is True else 0
        end_index = path_file.find('_')
        return path_file[start_index : end_index]

    def __move_file(self, src):
        key = self.__get_key(src)
        dir = directory_name.forder_list.get(key)
        if dir is not None:
            dst_path = f'{self.dst_root_path}{dir}'
            if os.path.isdir(dst_path) :
                if os.path.isfile(f'{dst_path}/{src}') is False :
                    shutil.move(f'{self.src_path}/{src}', dst_path)
                    return f"{src} \t ... ok"
                else : 
                    return f"{src} \t ... fail(exist file)"
            else :
                    return f"{src} \t ... fail(no directory)"
                
        else : 
            return f"{src} \t ... fail(new company)"
            
        

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
        

mov = MoveFile('./fax_receive/','./fax_receive/')

mov.run()
