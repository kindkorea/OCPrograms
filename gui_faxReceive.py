from tkinter import *
import os
import glob
import lib_faxReceive
from tkinter import simpledialog
import tkinter.messagebox as msg
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from queue import Queue

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
    def __init__(self, container):
        super().__init__(container )
        
        # self.file_listbox
        self.__create_widgets()
        
    def __create_widgets(self):
        self.FAX_DIRECTOR_PATH = 'C:/Users/kindk/OneDrive/OCWOOD_OFFICE/FAX_received/'
        # self.FAX_DIRECTOR_PATH = 'C:/Users/kindk/.vscode/test/'
        
        self.FAX_R = lib_faxReceive.FaxReceive(self.FAX_DIRECTOR_PATH)

        self.file_listbox = Listbox(self, width=50,  selectmode=SINGLE, highlightthickness=1) 
        self.file_listbox.grid(row=0,column=0) 
        
        self.scrollbar=Scrollbar(self, orient='vertical' ,command=self.file_listbox.yview)
        self.scrollbar.grid(row=0, sticky='nse')
        
        self.file_listbox.config(yscrollcommand = self.scrollbar.set)
        
        self.file_listbox.bind("<Key>",self.__handler_key)
        self.file_listbox.bind("<Double-Button-1>",self.__handler_double_button1)
        self.file_listbox.bind("<<ListboxSelect>>",self.__handler_ListboxSelect)
        
        self.btn_frame = Frame(self)
        self.refile_name = Entry(self.btn_frame,width=15)
        self.refile_name.grid(row=0 ,column=0, padx=10 )
        Button(self.btn_frame,width=10, text="RE:name" , command=self.__func_rename).grid(row=0 ,column=2) 
        Button(self.btn_frame,width=10,  text="Check" , command=self.__func_check).grid(row=0 ,column=3) 
        Button(self.btn_frame,width=10,  text="Delete" , command=self.__func_delete).grid(row=0 ,column=4)
        self.btn_frame.grid(row=1,column=0)
        self.__reset_listbox()
        
        # Observer 생성
        handler = CustomHandler(self)
        self.observer = Observer()
        self.observer.schedule(handler, self.FAX_DIRECTOR_PATH, recursive=True)
        self.queue = Queue()
        self.observer.start()
    
    def __handler_key(self, event):
        
        code = event.keycode
        print(code)
        if code == 46:  #key : del
            self.__func_delete()
        elif code == 113: #key : F2
            self.__func_rename()
        elif code == 13: #key : enter
            self.__run_with_viewer()
        # elif code == 38:  #key : up
        #     print('up')     
        # elif code == 40:  #key : down
        #     print('down')     

    def __selected_listbox_item(self):
        index = self.file_listbox.curselection()[0]
        print(f'__selected_src_file={index=}')
        if index is not None: # if the tuple is not empty
            return self.file_listbox.get(index)

    def __set_select_items(self):
        print(f'__set_select_items')
        self.FAX_R.selectitem = self.__selected_listbox_item()
        print(f'{self.FAX_R.selectitem=}')
        
    
    def __run_with_viewer(self):
        self.__set_select_items()
        self.FAX_R.Run_with_viewer()
        
    def __handler_double_button1(self, event):
        self.__run_with_viewer()
        print(f'__handler_double_button1')
    
   
    def __handler_ListboxSelect(self , event):
        print(f'__handler_ListboxSelect')
        self.__set_select_items()
        
    def __reset_listbox(self):
        self.file_listbox.delete(0,END)
        unchecked, checked = self.FAX_R.get_faxfiles()
        self.__set_listbox_data(checked, True)
        self.__set_listbox_data(unchecked, False)
        
    def __set_listbox_data(self, file_list , state):
        for f in file_list:
            self.file_listbox.insert(0,f'{os.path.basename(f)}')
        if state == True:
            for i in range(len(file_list)):
                self.file_listbox.itemconfig(i, {'fg':'gray'})
    
    def __func_check(self):
        self.__set_select_items()
        self.FAX_R.Checking_file()
        self.__reset_listbox()
        
    def __func_delete(self):
        self.__set_select_items()
        self.FAX_R.Delete_file()
        self.__reset_listbox()
    
    def __func_rename(self):     
        dst_filename = self.refile_name.get()
        if dst_filename == '' or dst_filename == None:
            dst_filename = self.__popup_asking_filename()
            print(dst_filename)       
            if dst_filename == '' or dst_filename == None:
                return
        self.__set_select_items()
        self.FAX_R.Rename_file(dst_filename)
        self.__reset_listbox()
        self.refile_name.delete(0,END)
  
    def __popup_asking_filename(self):
        # the input dialog
        USER_INP = simpledialog.askstring(title="팩스 이름 수정",
                                    prompt="이름을 입력하시오?")
         # check it out
        return USER_INP
    

        
    def popup_window(self, src_file):
        toplevel = Toplevel(self)

        toplevel.title("수신 팩스")
        toplevel.geometry("230x100+2000+10")


        l1=Label(toplevel, image="::tk::icons::question")
        l1.grid(row=0, column=0)
        l2=Label(toplevel,text="팩스 수신 완료")
        l2.grid(row=0, column=1, columnspan=3)

        b1=Button(toplevel ,text= "팩스 확인" , command= lambda:self.__btn_open_faxfile( toplevel, src_file))
        b1.grid(row=1, column=1)
        b2=Button(toplevel,text="닫기",command=toplevel.destroy, width=10)
        b2.grid(row=1, column=2)
    
    def __btn_open_faxfile(self, w, src_file):
        
        self.FAX_R.selectitem = os.path.basename(src_file)
        self.FAX_R.Run_with_viewer()
        self.__reset_listbox()   
        w.destroy()
    
    """Forward events from watchdog to GUI"""
    def notify_creation(self,event):
        print(f'file created{event.src_path}' )
        
        if event.src_path.endswith('.jpg'):
            self.popup_window(event.src_path)
    
    def notify(self, event):
        
        self.queue.put(event)
        self.__reset_listbox()      
            
















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
        
        # fax_path = 'C:/Users/kindk/OneDrive/OCWOOD_OFFICE/FAX_received/'
        fax_receive = GUI_FaxReceive(self)
        fax_receive.grid(column=0, row=1)
        # # create the button frame
        # button_frame = gui_pdf2jpg.Cb_Btn_frame(self,8)
        # button_frame.grid(column=0, row=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()        