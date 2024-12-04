import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES

def on_drop(event):
    # 드래그 앤 드롭으로 받아온 파일 경로 출력
    file_path = event.data
    # label.config(text=f"File dropped:\n{file_path}")
    print(file_path)

# TkinterDnD를 포함한 Tkinter 윈도우 생성
root = TkinterDnD.Tk()

# frame_test = tk.Frame
root.title("Drag and Drop Example")
root.geometry("400x200")

label = tk.Label(root, text="Drag and drop a file here", bg="lightblue", wraplength=350)
label.pack(expand=True, fill="both")

label = tk.Listbox(root)
label.pack(expand=True, fill="both")


# 드래그 앤 드롭 이벤트 바인딩
label.drop_target_register(DND_FILES)
label.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
