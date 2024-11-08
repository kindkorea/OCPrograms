import tkinter as tk
from tkinter import filedialog
from configparser import ConfigParser
import os
class SettingsApp(tk.Frame):
    def __init__(self, master , config_file, section, key):
        super().__init__(master)
        self.master = master
        # self.grid()
        self.config_file = config_file
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
            self.configure_phaser(folder_path)
            
            
    def configure_phaser_read(self):
        config = ConfigParser()
        if os.path.exists(self.config_file):
            print(self.config_file)
            config.read(self.config_file, encoding='utf-8')
            if config.has_section(self.config_section) and self.config_key in config[self.config_section]:
                folder_path = config[self.config_section][self.config_key]
                self.entry.insert(0,folder_path)
                
                    
        
    def configure_phaser(self, folder_path):
        config = ConfigParser()
        # config_file = 'settings.ini'

        # 기존 설정 파일이 있으면 읽어오기
        if os.path.exists(self.config_file):
            config.read(self.config_file,encoding="utf-8")

        # 'Phaser' 섹션이 있으면 업데이트, 없으면 새로 추가
        if not config.has_section(self.config_section):
            config.add_section(self.config_section)

        # 'FolderPath' 항목 갱신
        config[self.config_section][self.config_key] = folder_path
        
        # 갱신된 설정을 settings.ini 파일에 저장
        with open(self.config_file, 'w', encoding="utf-8") as configfile:
            config.write(configfile)
            
            
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Settings App")
    a = tk.Frame(root)
    a.grid(row=0,column=0)
    toJpg = SettingsApp(a,'./settings.ini', 'pdf parser','toJpg')
    changingName = SettingsApp(a,'./settings.ini', 'pdf parser','changingName')
    # app = SettingsApp(a,'./settings.ini', 'pdf parser','toJpg')
    
    
    toJpg.grid(row=0,column=0)
    changingName.grid(row=1,column=0)
    root.mainloop()
