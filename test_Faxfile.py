import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



class PopupWindow:
    def __init__(self, master, handler):
        self.master = master
        self.handler = handler
        self.popup_window = tk.Toplevel(master)
        self.popup_window.title("Popup Window")

        # 리스트박스1 생성
        self.listbox1 = tk.Listbox(self.popup_window, selectmode=tk.SINGLE)
        self.listbox1.pack(padx=10, pady=10)

        # 리스트박스1에 값 추가
        for i in range(1, 6):
            self.listbox1.insert(tk.END, f"Item {i}")

        # 확인 버튼
        btn_ok = tk.Button(self.popup_window, text="OK", command=self.on_ok_button)
        btn_ok.pack(pady=10)

    def on_ok_button(self):
        selected_index = self.listbox1.curselection()
        if selected_index:
            selected_value = self.listbox1.get(selected_index)
            messagebox.showinfo("Selected Value", f"Selected Value: {selected_value}")
            self.handler(selected_value)
            self.popup_window.destroy()

            
            
class FileListApp(tk.Frame):
    def __init__(self, container):
        super().__init__( container)
        
        # self.root = root
        # self.root.title("File List App")

        # 1행: 리스트박스1, 스크롤바
        self.listbox1 = tk.Listbox(self, selectmode=tk.SINGLE)
        self.listbox1.grid(row=0, column=0)

        scrollbar1 = tk.Scrollbar(self, command=self.listbox1.yview)
        scrollbar1.grid(row=0, column=0)
        self.listbox1.config(yscrollcommand=scrollbar1.set)

        self.listbox1.bind('<<ListboxSelect>>', self.on_listbox1_select)

        

        # 특정 폴더의 파일을 시간 순서로 리스트박스1에 출력
        folder_path = filedialog.askdirectory(title="Select Folder")
        self.populate_listbox1(folder_path)
        
        # 파일 변화 감지
        self.event_handler = FileChangeHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path=folder_path, recursive=False)
        self.observer.start()
        
        # # 2행: 엔트리1, 리스트박스2, 스크롤바
        # entry1_frame = tk.Frame(root)
        # entry1_frame.pack(side=tk.LEFT, padx=10)

        # self.entry1 = tk.Entry(entry1_frame)
        # self.entry1.pack(pady=10)

        # self.listbox2 = tk.Listbox(root, selectmode=tk.SINGLE)
        # self.listbox2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # scrollbar2 = tk.Scrollbar(root, command=self.listbox2.yview)
        # scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        # self.listbox2.config(yscrollcommand=scrollbar2.set)

        # self.listbox2.bind('<<ListboxSelect>>', self.on_listbox2_select)

        # 2행 버튼
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=1)

        btn_rename = tk.Button(button_frame, text="Re:name", command=self.rename_file)
        btn_rename.pack(pady=5)

        btn_check = tk.Button(button_frame, text="Check", command=self.check_file)
        btn_check.pack(pady=5)

        btn_delete = tk.Button(button_frame, text="Delete", command=self.delete_file)
        btn_delete.pack(pady=5)

        btn_move = tk.Button(button_frame, text="Move", command=self.move_file)
        btn_move.pack(pady=5)

        btn_move_all = tk.Button(button_frame, text="MoveAll", command=self.move_all_files)
        btn_move_all.pack(pady=5)
        
        
        self.gird(row=0, column=0)

    def populate_listbox1(self, folder_path):
        files = sorted(os.listdir(folder_path), key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
        self.listbox1.delete(0, tk.END)
        for file in files:
            self.listbox1.insert(tk.END, file)

    def on_listbox1_select(self, event):
        selected_index = self.listbox1.curselection()
        if selected_index:
            selected_file = self.listbox1.get(selected_index)
            print(f"Selected File in Listbox1: {selected_file}")

    def on_listbox2_select(self, event):
        selected_index = self.listbox2.curselection()
        if selected_index:
            selected_file = self.listbox2.get(selected_index)
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, selected_file)

    def rename_file(self):
        
        popup = PopupWindow(self.root , self.get_filename)
        # selected_index = self.listbox1.curselection()
        # if selected_index:
        #     selected_file = self.listbox1.get(selected_index)
        #     new_name = self.entry1.get()
        #     new_path = os.path.join(os.path.dirname(selected_file), new_name)
        #     os.rename(selected_file, new_path)
        #     self.populate_listbox1(os.path.dirname(selected_file))
    def get_filename(self,filename):
        print(filename)
        
        
    def check_file(self):
        keyword = self.entry1.get().lower()
        self.listbox2.delete(0, tk.END)
        for file in os.listdir('.'):
            if keyword in file.lower():
                self.listbox2.insert(tk.END, file)

    def delete_file(self):
        selected_index = self.listbox1.curselection()
        if selected_index:
            selected_file = self.listbox1.get(selected_index)
            os.remove(selected_file)
            self.populate_listbox1(os.path.dirname(selected_file))

    def move_file(self):
        selected_index = self.listbox1.curselection()
        if selected_index:
            selected_file = self.listbox1.get(selected_index)
            target_folder = filedialog.askdirectory(title="Select Target Folder")
            shutil.move(selected_file, os.path.join(target_folder, os.path.basename(selected_file)))
            self.populate_listbox1(os.path.dirname(selected_file))

    def move_all_files(self):
        target_folder = filedialog.askdirectory(title="Select Target Folder")
        for file in self.listbox1.get(0, tk.END):
            shutil.move(file, os.path.join(target_folder, os.path.basename(file)))
        self.populate_listbox1(target_folder)

    def reset_listbox1(self, folder_path):
        self.populate_listbox1(folder_path)

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_any_event(self, event):
        if event.is_directory or event.event_type == 'modified':
            return
        self.app.reset_listbox1(os.path.dirname(event.src_path))


class PopupWindow:
    def __init__(self, master, handler):
        self.master = master
        self.handler = handler
        self.popup_window = tk.Toplevel(master)
        self.popup_window.title("Popup Window")

        # 리스트박스1 생성
        self.listbox1 = tk.Listbox(self.popup_window, selectmode=tk.SINGLE)
        self.listbox1.pack(padx=10, pady=10)

        # 리스트박스1에 값 추가
        for i in range(1, 6):
            self.listbox1.insert(tk.END, f"Item {i}")

        # 확인 버튼
        btn_ok = tk.Button(self.popup_window, text="OK", command=self.on_ok_button)
        btn_ok.pack(pady=10)

    def on_ok_button(self):
        selected_index = self.listbox1.curselection()
        if selected_index:
            selected_value = self.listbox1.get(selected_index)
            messagebox.showinfo("Selected Value", f"Selected Value: {selected_value}")
            self.handler(selected_value)
            self.popup_window.destroy()





class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('웅천목재 프로그램')
        self.geometry('600x800')

    


if __name__ == "__main__":
    app = App()
    FileListApp(app)
    
    app.mainloop()
    
    
