from tkinter import *
import os
import glob
import lib_faxReceive
from tkinter import simpledialog
import tkinter.messagebox as msg
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from queue import Queue
import directory_name


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
        super().__init__(container)
        
        
        
        self.container = self
        # self.grid(row=row, column=col , pady=20)
        # self.file_listbox
        self.__create_widgets()
        
    def __create_widgets(self):
        self.FAX_DIRECTOR_PATH = 'C:/Users/kindk/OneDrive/OCWOOD_OFFICE/FAX_received/'
        # self.FAX_DIRECTOR_PATH = './fax_receive/'
        
        if os.path.isdir(self.FAX_DIRECTOR_PATH) == False:
            print(f'Fax Directory [{self.FAX_DIRECTOR_PATH}] is not existed')
            return            
        
        self.FAX_R = lib_faxReceive.FaxReceive(self.FAX_DIRECTOR_PATH)

        self.file_listbox = Listbox(self.container, width=50,  selectmode=SINGLE, highlightthickness=1) 
        self.file_listbox.grid(row=0,column=0) 
        
        self.scrollbar=Scrollbar(self.container, orient='vertical' ,command=self.file_listbox.yview)
        self.scrollbar.grid(row=0, sticky='nse')
        
        self.file_listbox.config(yscrollcommand = self.scrollbar.set)
        
        self.file_listbox.bind("<Key>",self.__handler_bind_key_from_file_listbox)
        self.file_listbox.bind("<Double-Button-1>",self.__handler_bind_double_button1_from_file_listbox)
        self.file_listbox.bind("<<ListboxSelect>>",self.__handler_bind_ListboxSelect_from_file_listbox)
        
        
       
        
        
        # menu of file rename
        self.btn_frame = LabelFrame(self.container, text='Choose Company')
        
        # Button(self.btn_frame, width=13, text="RE:name" , command=self.__func_rename).grid(row=0 ,column=1, padx= 10 ,sticky='ew') 
        # Button(self.btn_frame, width=13,  text="Check" , command=self.__func_check).grid(row=0 ,column=2,padx= 10 ,sticky='ew') 
        # Button(self.btn_frame, width=13,  text="Delete" , command=self.__func_delete).grid(row=0 ,column=3,padx= 10 ,sticky='ew')
        
        self.btn_frame.grid(row=1,column=0,pady = 10)
       
        
        Button(self.btn_frame, width=13, text="RE:name" , command=self.__handler_btn_rename).grid(row=0,column=1, padx= 10 ,sticky='nsew') 
        Button(self.btn_frame, width=13,  text="Check" , command=self.__handler_btn_check).grid(row=1 ,column=1,  padx= 10 ,sticky='nsew') 
        Button(self.btn_frame, width=13,  text="Delete" , command=self.__handler_btn_delete).grid(row=2 ,column=1,padx= 10 ,sticky='nsew')
        Button(self.btn_frame, width=13,  text="Move" , command=self.__handler_btn_file_move).grid(row=3 ,column=1,  padx= 10 ,sticky='nsew')
        Button(self.btn_frame, width=13,  text="MoveAll" , command=self.__handler_btn_file_move_all).grid(row=4 ,column=1,padx= 10 ,sticky='nsew')
        
        self.company_name = directory_name.CompanyListWidget(self.btn_frame,directory_name.CompanyList.keys(), self.__handler_company_rename)
        # app.Set_handler(event, self.__func_rename)
        self.company_name.grid(row=0, column=0, padx= 10, rowspan=5)
        self.to_change_company_name = StringVar()
        self.__reset_listbox()
        # Observer 생성
        handler = CustomHandler(self)
        self.observer = Observer()
        self.observer.schedule(handler, self.FAX_DIRECTOR_PATH, recursive=True)
        self.queue = Queue()
        self.observer.start()
        
    

    def __get_selected_file_from_listbox(self):  # get file from listbox
        selected_tuple = self.file_listbox.curselection()
        return False if not selected_tuple else self.file_listbox.get(selected_tuple[0])


    def __set_selected_file(self):  # setting target file
        select_file = self.__get_selected_file_from_listbox()
        if select_file : 
            self.FAX_R.selectitem = select_file
            return True
        else :
            return False
            
    def __run_with_viewer(self):  # run viewer 
        if self.__set_selected_file() :
            self.FAX_R.Run_with_viewer()
        else :
            print('error : __run_with_viewer ')
        

    def __reset_listbox(self):
        self.file_listbox.delete(0,END)
        unchecked, checked = self.FAX_R.get_faxfiles()
        self.__set_list_to_listbox(checked, True)
        self.__set_list_to_listbox(unchecked, False)
        
    def __set_list_to_listbox(self, file_list , state):
        for f in file_list:
            self.file_listbox.insert(0,f'{os.path.basename(f)}')
        if state == True:
            for i in range(len(file_list)):
                self.file_listbox.itemconfig(i, {'fg':'gray'})
    

    def __rename(self, filename):
        if filename == '' or filename == None:
            return False
        
        if self.FAX_R.selectitem == '' :
            return False
        else : 
            self.FAX_R.Rename_file(filename)
            self.__reset_listbox()
            return True
           
        

        
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
    
    def __handler_bind_key_from_file_listbox(self, event):
        
        code = event.keycode
        print(code)
        if code == 46:  #key : del
            self.__func_delete()
        elif code == 113: #key : F2
            self.company_name.search.focus()
        elif code == 13: #key : enter
            self.__run_with_viewer()
        # elif code == 38:  #key : up
        #     print('up')     
        # elif code == 40:  #key : down
        #     print('down')     
    
    def __handler_bind_double_button1_from_file_listbox(self, event):  
        self.__run_with_viewer()
    
    def __handler_bind_ListboxSelect_from_file_listbox(self , event):
        # if not self.file_listbox.curselection():  # ignore empty tuple
        #     return
        self.__set_selected_file()
        
    def __handler_company_rename(self, f_name):
        # print(f'__handler_company_rename{f_name}')        
         self.to_change_company_name = f_name
        
    def __handler_btn_check(self):
        if self.__set_selected_file() :
            self.FAX_R.Checking_file()
            self.__reset_listbox()
        else :
            print(f'error : __handler_btn_check')        

    
    def __handler_btn_delete(self):
        if self.__set_selected_file() :
            self.FAX_R.Delete_file()
            self.__reset_listbox()
        else :
            print(f'error : __handler_btn_delete')        
    
    def __handler_btn_rename(self):    
        
        getName 
        self.__rename(self.to_change_company_name)
        print("__handler_btn_rename")

    def __handler_btn_file_move(self):     
        print("__handler_btn_file_move")
        
        
    def __handler_btn_file_move_all(self):     
        print("__handler_btn_file_move_all")















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