import tkinter as tk
from tkinter import filedialog
from configparser import ConfigParser
import os
class SettingsApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # self.grid()
        self.config_file = 'settings.int'
        self.create_widgets()
        self.configure_phaser_read()
    
    def create_widgets(self):
        # Label
        self.label = tk.Label(self, text="Folder Path:")
        self.label.grid(row=0, column=0)
        
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
            config.read(self.config_file, encoding='utf-8')
            if config.has_section('Phaser') and 'FolderPath' in config['Phaser']:
                folder_path = config['Phaser']['FolderPath']
                self.entry.insert(0,folder_path)
                
                    
        
    def configure_phaser(self, folder_path):


        config = ConfigParser()
        config_file = 'settings.ini'

        # 기존 설정 파일이 있으면 읽어오기
        if os.path.exists(config_file):
            config.read(config_file,encoding="utf-8")

        # 'Phaser' 섹션이 있으면 업데이트, 없으면 새로 추가
        if not config.has_section('Phaser'):
            config.add_section('Phaser')

        # 'FolderPath' 항목 갱신
        config['Phaser']['FolderPath'] = folder_path
        
        # 갱신된 설정을 settings.ini 파일에 저장
        with open(config_file, 'w', encoding="utf-8") as configfile:
            config.write(configfile)
            
            
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Settings App")
    a = tk.Frame(root)
    a.grid(row=0,column=0)
    app = SettingsApp(a)
    app.grid(row=0,column=0)
    app.mainloop()
