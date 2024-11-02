import tkinter as tk
from tkinter import filedialog
import configparser






class SettingsApp:
    def __init__(self, root):
        self.root = root
        # self.root.title("Settings App")
        
        self.frame_setting = tk.LabelFrame(self.root, text='PDF 파일')
        self.frame_setting.grid(row=0, column=0)
        # 결과 레이블
        tk.Label(self.frame_setting, text="불러올 PDF : ").grid(row=0,column=0)
        # self.result_label.pack(pady=10)
        # 파일 선택 버튼
        self.select_button = tk.Button(self.frame_setting, text="폴더열기", command=lambda x = 'get' : self.select_folder(x))
        self.select_button.grid(row=0, column=1)
        
        # 결과 레이블
        self.result_label = tk.Label(self.frame_setting, text="No folder selected")
        self.result_label.grid(row=1, column=1)
    
    
    
    
    def select_folder(self , key):
        # 폴더 선택 대화상자 열기
        folder_path = filedialog.askdirectory()
        if folder_path:  # 사용자가 폴더를 선택한 경우
            # 선택된 경로를 레이블에 표시
            self.result_label.config(text=f"Selected Folder: {folder_path}")
            # return folder_path
            # 설정을 .ini 파일로 저장
            self.save_to_ini(key ,folder_path)
    
    def save_to_ini(self,key, folder_path):
        # ConfigParser 객체 생성
        config = configparser.ConfigParser()
        
        # 'Settings' 섹션에 폴더 경로 저장
        config[key] = {key : folder_path}
        
        # .ini 파일로 저장
        with open("settings.ini", "w", encoding="utf-8") as configfile:
            config.write(configfile)
        
        print("Folder path saved to settings.ini")

# 프로그램 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsApp(root)
    root.mainloop()
