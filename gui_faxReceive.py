
from tkinter import *
import os
import glob
import lib_faxReceive
from tkinter import simpledialog
import tkinter.messagebox as msg
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from queue import Queue

import sys
import subprocess


class CustomHandler(FileSystemEventHandler):
    def __init__(self, app):
        FileSystemEventHandler.__init__(self)
        self.app = app
    def on_created(self, event):     
        self.app.notify_creation(event)
        
    def on_deleted(self, event): self.app.notify(event)
    def on_modified(self, event): self.app.notify(event)
    def on_moved(self, event): self.app.notify(event)



class GUI_FaxReceive(Frame):
    def __init__(self, container , fax_path):
        super().__init__(container )
        
        
        
        self.DIRECTOR_PATH = fax_path
        self.extention_viewer = 'c:/Users/kindk/AppData/Local/Imagine/Imagine64.exe'
        # self.file_listbox
        self.__create_widgets()
        
        
    def __create_widgets(self):
        
        
        
        self.FAX_R = lib_faxReceive.FaxReceive(self.DIRECTOR_PATH)

        

        self.file_listbox = Listbox(self, width=50,  selectmode=SINGLE, highlightthickness=1) 
        self.file_listbox.grid(row=0,column=0) 
        
        self.scrollbar=Scrollbar(self, orient='vertical' ,command=self.file_listbox.yview)
        self.scrollbar.grid(row=0, sticky='nse')
        
        self.file_listbox.config(yscrollcommand = self.scrollbar.set)
        
        self.file_listbox.bind("<Key>",self.__handler_key)
        self.file_listbox.bind("<Double-Button-1>",self.__handler_mouse)
        
        self.btn_frame = Frame(self)
        self.refile_name = Entry(self.btn_frame,width=15)
        self.refile_name.grid(row=0 ,column=0, padx=10 )
        # Checkbutton(self.btn_frame,width=10,  text="Checked").grid(row=0 ,column=1) 
        Button(self.btn_frame,width=10, text="RE:name" , command=self.__func_rename).grid(row=0 ,column=2) 
        Button(self.btn_frame,width=10,  text="Check" , command=self.__func_check).grid(row=0 ,column=3) 
        Button(self.btn_frame,width=10,  text="Delete" , command=self.__func_delete).grid(row=0 ,column=4)
        self.btn_frame.grid(row=1,column=0)
        self.__reset_listbox()
        
        # Observer 생성
        handler = CustomHandler(self)
        self.observer = Observer()
        self.observer.schedule(handler, self.DIRECTOR_PATH, recursive=True)
        self.queue = Queue()
        self.observer.start()
        
    
    def __handler_key(self, event):
        
        code = event.keycode
        print(code)
        if code == 46:  #key : del
            # print("function : rename")
            self.__func_delete()
        elif code == 113: #key : F2
            self.__func_rename()
        elif code == 13: #key : enter
            f  = self.__selected_src_file()
            self.__run_with_viewer(f)
        # elif code == 38:  #key : up
        #     print('up')     
        # elif code == 40:  #key : down
        #     print('down')     

    def __handler_mouse(self,event):
        if not event.widget.curselection():
            return
        f  = self.__selected_src_file()
        self.__run_with_viewer(f)
        
        
    def __reset_listbox(self):
        unchecked, checked = self.FAX_R.get_faxfiles()
        self.__set_listbox_data(unchecked,checked)
    
    def __set_listbox_data(self, unchecked_files, checked_files):
        self.file_listbox.delete(0,END)
        for f in checked_files:
            self.file_listbox.insert(0,f'{os.path.basename(f)}')
            
        for f in unchecked_files:
            self.file_listbox.insert(0,f'{os.path.basename(f)}')
        
        for i in range(len(checked_files)):
            self.file_listbox.itemconfig(len(unchecked_files)+i, {'fg':'gray'})
    
    def __func_check(self):
        print('checked')
        f = self.__selected_src_file()
        
        self.FAX_R.Checking_file(f)
        self.__reset_listbox()
        
        
        
    def __func_delete(self):
        f = self.__selected_src_file()
        self.FAX_R.Delete_file(f)
        self.__reset_listbox()
        
    def __selected_src_file(self):
        index = self.file_listbox.curselection()[0]
        if index is not None: # if the tuple is not empty
            return f'{self.DIRECTOR_PATH}{self.file_listbox.get(index)}'
    
    
    
    def __func_rename(self):     
        src_file = self.__selected_src_file()
        if src_file is None:
            msg.showinfo(title='Re:name', message='No chose file')
            return
        
        dst_filename = self.refile_name.get()
        if dst_filename == '':
            dst_filename = self.__popup_asking_filename()
        
        if dst_filename == '':
            return
        print(f'__func_rename : {src_file=}, {dst_filename=}')
        self.FAX_R.Rename_file( src_file, dst_filename)
        self.__reset_listbox()
        self.refile_name.delete(0,END)

    

    def __run_with_viewer(self, src_file):
        cmd = f'{self.extention_viewer} {src_file}'
        print(f'__run_with_viewer = {cmd}')
        subprocess.Popen(cmd)
  
    def __popup_asking_filename(self):
        # the input dialog
        USER_INP = simpledialog.askstring(title="Test",
                                    prompt="What's your Name?:")
         # check it out
        return USER_INP
    
    def notify(self, event):
        """Forward events from watchdog to GUI"""
        self.queue.put(event)
        self.__reset_listbox()      
        
    def popup_window(self, src_file):
        toplevel = Toplevel(self)

        toplevel.title("Kill window")
        toplevel.geometry("230x100+2000+10")


        l1=Label(toplevel, image="::tk::icons::question")
        l1.grid(row=0, column=0)
        l2=Label(toplevel,text="Are you sure you want to Quit")
        l2.grid(row=0, column=1, columnspan=3)

        b1=Button(toplevel ,text= "팩스 확인" , command= lambda:self.__btn_open_faxfile( toplevel, src_file))
        b1.grid(row=1, column=1)
        b2=Button(toplevel,text="닫기",command=toplevel.destroy, width=10)
        b2.grid(row=1, column=2)
    
    def __btn_open_faxfile(self, w, srcfile):
        self.__run_with_viewer(srcfile)
        w.destroy()
        
    
    def notify_creation(self,event):
        print(f'file created{event.src_path}' )
        # self.__run_with_viewer(event.src_path)
        # msg.showinfo(title='Fax Receive', message='팩스가 도착하였습니다.')
        self.popup_window(event.src_path)
            
            
















class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Replace')
        self.geometry('500x500+2000+100')
        # self.resizable(0, 0)
        # windows only (remove the minimize/maximize button)
        # self.attributes('-toolwindow', True)

        # layout on the root window
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        # create the input frame
        # input_frame = gui_pdf2jpg.Pdf2jpg(self,8)
        # input_frame.grid(column=0, row=0)
        fax_path = 'C:/Users/kindk/.vscode/test/'
        # fax_path = 'C:/Users/kindk/OneDrive/OCWOOD_OFFICE/FAX_received/'
        fax_receive = GUI_FaxReceive(self,fax_path)
        fax_receive.grid(column=0, row=1)
        # # create the button frame
        # button_frame = gui_pdf2jpg.Cb_Btn_frame(self,8)
        # button_frame.grid(column=0, row=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()        