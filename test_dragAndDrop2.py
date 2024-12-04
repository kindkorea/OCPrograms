import os
import shutil
from tkinter import Tk,Button, Listbox, filedialog, messagebox, END
from tkinterdnd2 import TkinterDnD, DND_FILES

def add_files():
    """사용자가 선택한 폴더의 파일을 Listbox에 추가"""
    folder = filedialog.askdirectory()
    if folder:
        file_listbox.delete(0, END)
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                file_listbox.insert(END, file_path)

def on_drag(event):
    """드래그된 파일 경로 가져오기"""
    files = event.data.strip("{}").split()
    if files:
        target_directory = filedialog.askdirectory(title="파일을 저장할 폴더 선택")
        if target_directory:
            for file in files:
                try:
                    shutil.copy(file, target_directory)
                    messagebox.showinfo("성공", f"파일이 {target_directory}로 복사되었습니다.")
                except Exception as e:
                    messagebox.showerror("오류", f"파일 복사 실패: {e}")

# 메인 윈도우 생성
root = TkinterDnD.Tk()
root.title("Drag and Drop Listbox")
root.geometry("600x400")

# 파일 리스트를 보여줄 Listbox
file_listbox = Listbox(root, selectmode="extended", width=80, height=20)
file_listbox.pack(pady=10)

# 파일 추가 버튼
add_button = Listbox(root, height=1)
add_button.bind('<Return>', add_files)
add_button.insert(END,' 파일 및 추가하실 수 원리 ')

# 파일 추가 버튼
add_button = Button(root, text="폴더 선택", command=add_files)
add_button.pack(pady=5)

# 드래그 앤 드롭 지원 설정
file_listbox.drop_target_register(DND_FILES)
file_listbox.dnd_bind("<<Drop>>", on_drag)

root.mainloop()
