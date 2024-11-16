import tkinter as tk
from tkinter import filedialog
import configparser
import json


import tkinter as tk
from tkinter import filedialog
from configparser import ConfigParser
import os

import json


class JsonReader():
    @staticmethod
    def read(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file :
            return json.load(json_file)
    @staticmethod
    def write(json_file_path, data):
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False ,indent=4)
            

    @staticmethod
    def is_data(json_file_path, key, data):
        temp_data = JsonReader.read(json_file_path)
        if key in temp_data :
            if  data in temp_data[key] :
                return temp_data
        return False
            
        
    @staticmethod
    def is_key(json_file_path, key):
        temp_data = JsonReader.read(json_file_path)
        if key in temp_data:
            return temp_data
        else :
            return False  
    
    @staticmethod
    def move(json_file_path , from_key, to_key, move_data):
        temp_data = JsonReader.read(json_file_path)
        if from_key in temp_data and move_data in temp_data[from_key] :
            # print(f'there is {move_data}')
            temp_data[to_key].append(move_data)
            temp_data[from_key].remove(move_data)
            JsonReader.write(json_file_path,temp_data)

    @staticmethod
    def add(json_file_path , key, data):
        temp_data = JsonReader.read(json_file_path)
        try :
            if not data in temp_data[key] :
                temp_data[key].append(data)
                JsonReader.write(json_file_path,temp_data)
            else :
                print(f"{data} is already Existed")
        except : 
            pass

            
            
class ConfigureIni():
    @staticmethod
    def read(config_section, config_key):
        config_file = 'settings.ini'
        config = ConfigParser()
        if os.path.exists(config_file):
            # print(config_file)
            config.read(config_file, encoding='utf-8')
            if config.has_section(config_section) and config_key in config[config_section]:
                return config[config_section][config_key]

    @staticmethod
    def write(config_section, config_key ,value):
        config_file = 'settings.ini'
        config = ConfigParser()
        # config_file = 'settings.ini'

        # 기존 설정 파일이 있으면 읽어오기
        if os.path.exists(config_file):
            config.read(config_file,encoding="utf-8")

        # 'Phaser' 섹션이 있으면 업데이트, 없으면 새로 추가
        if not config.has_section(config_section):
            config.add_section(config_section)

        # 'FolderPath' 항목 갱신
        config[config_section][config_key] = value
        
        # 갱신된 설정을 settings.ini 파일에 저장
        with open(config_file, 'w', encoding="utf-8") as config_file:
                 config.write(config_file)
                 
    @staticmethod         
    def read_and_return_list(config_section, config_key):
        read_file = ConfigureIni.read(config_section,config_key)
        if read_file : 
            # config.read(config_file, encoding='utf-8')
            return json.loads(read_file)



class SettingConfig(tk.Frame):
    def __init__(self, master , section, key):
        super().__init__(master)
        self.master = master
        # self.grid()
        # self.config_file = config_file
        self.config_section = section
        self.config_key = key
        
        self.create_widgets()
        self.configure_phaser_read()
    
    def create_widgets(self):
        # Label
        self.label = tk.Label(self,width=15, text= f'{self.config_key} : ')
        self.label.grid(row=0, column=0 ,sticky='we')
        
        # Entry
        self.entry = tk.Entry(self, width=50)
        self.entry.grid(row=0, column=1)
        
        # Button
        self.button = tk.Button(self, text="Browse", command=self.save_folder_path)
        self.button.grid(row=0, column=2)
    
    def save_folder_path(self):
        # 폴더 선택 대화상자 열기
        folder_path = filedialog.askdirectory()
        if folder_path:
            # 엔트리에 선택한 경로 표시
            self.entry.delete(0, tk.END)
            self.entry.insert(0, folder_path)
            # settings.ini 파일에 경로 저장
            ConfigureIni.write(self.config_section, self.config_key, folder_path)
            
            
    def configure_phaser_read(self):
    
        folder_path = ConfigureIni.read(self.config_section, self.config_key)
        if folder_path:
            self.entry.insert(0,folder_path)
                
           


class SettingsApp:
    def __init__(self, root):
        self.root = root
        # self.root.title("Settings App")
        
        self.frame_setting = tk.LabelFrame(self.root, text='PDF 파일')
        self.frame_setting.grid(row=0, column=0)
        
        
        from_pdf_folder = SettingConfig(self.frame_setting, 'pdf parser','from_pdf_folder')
        save_folder = SettingConfig(self.frame_setting, 'pdf parser','save_folder')
        fax_save_folder = SettingConfig(self.frame_setting, 'fax','fax_save_folder')
        # app = SettingsApp(a,'./settings.ini', 'pdf parser','toJpg')
        
        
        from_pdf_folder.grid(row=0,column=0)
        save_folder.grid(row=1,column=0)
        fax_save_folder.grid(row=2,column=0)


# 프로그램 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsApp(root)
    root.mainloop()
