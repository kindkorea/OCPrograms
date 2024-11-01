from tkinter import *
import os
import glob
import lib_faxReceive
from tkinter import simpledialog
import tkinter.messagebox as msg
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from queue import Queue
from tkinter import messagebox
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

class CompanyButtonApp:
    def __init__(self, root , callback ):
        self.root = root
        # self.root.title("Grid Button App")
        self.companies = [
            "건한",
            "나산팀버",
            "대한테이프",
            "두산종합목재",
            "삼원목재",
            "에스디팀버",
            "온보드",
            "우진프레임",
            "원스탑우드",
            "진양",
            "케이디우드",
            "크나우프",
            "태진목재",
            "한국산업"
        ]
        self.callback = callback
        self.create_buttons()

    def create_buttons(self):
        for index, title in enumerate(self.companies):
            row = index // 5
            column = index % 5
            button = Button(self.root, text=title, command=lambda x=title: self.callback(x))
            button.grid(row=row, column=column, padx=5, pady=5 , sticky='ew')

    # def button_action(self, button_number):
    #     print(f"{button_number}")
        
                        

class GUI_FaxReceive():
    def __init__(self, containerFrame):
        
        self.container = containerFrame
        
        self.selected_files = []
        self.__create_widgets()
        self.selected_file_from_Listbox = list()
        
    def __create_widgets(self):
        self.FAX_DIRECTOR_PATH = 'C:/Users/kindk/OneDrive/OCWOOD_OFFICE/FAX_received/'
        # self.FAX_DIRECTOR_PATH = './fax_receive/'  # test directory
       
        # menu of file rename
        self.fax_frame = LabelFrame(self.container, text='Choose Company')
        
        self.fax_frame.grid(row=0,column=0, padx=10 ,pady = 10)
        
        self.FAX_R = lib_faxReceive.FaxReceive(self.FAX_DIRECTOR_PATH)
        self.file_listbox = Listbox(self.fax_frame, width=30,  height=25, selectmode=EXTENDED, highlightthickness=1) 
        self.file_listbox.grid(row=0,column=0,rowspan=5) 
        
        self.scrollbar=Scrollbar(self.fax_frame, orient='vertical' ,command=self.file_listbox.yview)
        self.scrollbar.grid(row=0, column=1 , rowspan= 5, sticky='ns')
        
        self.file_listbox.config(yscrollcommand = self.scrollbar.set)
        
        self.file_listbox.bind("<Key>",self._handler_bind_key_from_file_listbox)
        self.file_listbox.bind("<Double-Button-1>",self._handler_doubleClick_from_file_listbox)
        
        Button(self.fax_frame, width=13,  text="열기(ENTER)" , command=self._run_with_viewer).grid(row=0 ,column=2,  padx= 10 ,sticky='nsew')
        Button(self.fax_frame, width=13, text="이름변경(F2)" , command=self._handler_rename_to_company).grid(row=1,column=2, padx= 10 ,sticky='nsew') 
        Button(self.fax_frame, width=13,  text="체크함" , command=self._handler_btn_check).grid(row=2 ,column=2,  padx= 10 ,sticky='nsew') 
        Button(self.fax_frame, width=13,  text="삭제(DEL)" , command=self._handler_btn_delete).grid(row=3 ,column=2,padx= 10 ,sticky='nsew')
        Button(self.fax_frame, width=13,  text="MoveAll" , command=self._handler_btn_file_move).grid(row=4 ,column=2,padx= 10 ,sticky='nsew')
        
        
        self.frameBtnCompanies = Frame(self.container)
        self.frameBtnCompanies.grid(row=1,column=0)
        CompanyButtonApp(self.frameBtnCompanies  , self._func_rename)
        
        
        self.to_change_company_name = StringVar()
        self._reset_listbox()
        
        
    def _func_rename(self, title):
        self.popup_handler_from_rename( title)
        
        # print(title)

    def _handler_doubleClick_from_file_listbox(self,e):
        self._run_with_viewer()
            
    def _run_with_viewer(self):  # run viewer 
        selected_file = self._get_from_file_listbox()
        if  selected_file : 
            for src_name in selected_file:
                self.FAX_R.run_with_viewer(src_name)
        else :
            print('self.selected_file_from_Listbox is empty')
        
    def _reset_listbox(self):
        self.file_listbox.delete(0,END)
        unchecked, checked = self.FAX_R.get_faxfiles()
        self._set_list_to_listbox(checked, True)
        self._set_list_to_listbox(unchecked, False)
        
    def _set_list_to_listbox(self, file_list , state):
        for f in file_list:
            self.file_listbox.insert(0,f'{os.path.basename(f)}')
        if state == True:
            for i in range(len(file_list)):
                self.file_listbox.itemconfig(i, {'fg':'gray'})
    
    
    """Forward events from watchdog to GUI"""
    def notify_creation(self,event):
        print(f'file created{event.src_path}' )
        

    
    def notify(self, event):
        
        self.queue.put(event)
        self._reset_listbox()      
    
    def _handler_bind_key_from_file_listbox(self, event):
        
        code = event.keycode
        # print(code)
        if code == 46:  #key : del
            self._handler_btn_delete()
            
        elif code == 113: #key : F2
            self._handler_rename_to_company()
            
        elif code == 114: #key : F3
            self._run_with_viewer()
            
        elif code == 13: #key : enter
            self._run_with_viewer()
            
            
        
        # elif code == 38:  #key : up
        #     print('up')     
        # elif code == 40:  #key : down
        #     print('down')     
    # def _handler_bind_ListboxSelect_from_file_listbox(self , event):
    #     selected_indices = self.file_listbox.curselection()
    #     if selected_indices :
    #         self.selected_file_from_Listbox = [self.file_listbox.get(idx) for idx in selected_indices]
        
    def _get_from_file_listbox(self):
        selected_indices = self.file_listbox.curselection()
        if selected_indices :
            return [self.file_listbox.get(idx) for idx in selected_indices]
        
        
    
    def _handler_rename_to_company(self):
        """ pop up window and get company name"""
        self.selected_files = self._get_from_file_listbox()
        if  self.selected_files: 
            directory_name.CompanyListWidget(self.container, self.popup_handler_from_rename )
    
    # def _handler_rename_to_company(self):
    #     """ pop up window and get company name"""
    #     self.selected_files = self._get_from_file_listbox()up_handler_from_rename )
    
    #     if  self.selected_files: 
    #         directory_name.CompanyListWidget(self.container, self.pop
        
    def popup_handler_from_rename(self, dst_name):
        if  self.selected_files: 
            for src_name in self.selected_files:
                # if msg.askyesno('파일 이름 변경', f'{src_name} => {dst_name}'):
                self.FAX_R.rename_to_company(src_name , dst_name)           
            self._reset_listbox()
        else :
            print('self.selected_file_from_Listbox is empty')
        
    
        
    def _handler_btn_check(self):
        selected_file = self._get_from_file_listbox()
        if  selected_file : 
            for src_name in selected_file:
                self.FAX_R.is_checked(src_name)           
            self._reset_listbox()
        else :
            print('self.selected_file_from_Listbox is empty')    
         
    def _handler_btn_delete(self):
        
        selected_file = self._get_from_file_listbox()
        if  selected_file : 
            for src_name in selected_file:
               
                if messagebox.askyesno('파일삭제', 
                                       f'{src_name}을 삭제할까요?',
                                        # parent=self,
                                        # geometry="+{}+{}".format(self.winfo_x(), self.winfo_y()),
                                       ) :
                    self.FAX_R.delete_file(src_name)           
            self._reset_listbox()
        else :
            print('self.selected_file_from_Listbox is empty')

    def _handler_btn_file_move(self):     
        # print("__handler_btn_file_move")
        selected_file = self._get_from_file_listbox()
        if  selected_file : 
            for src_name in selected_file:
                directory_name.FileMove(self , self.selected_file_from_Listbox ,self.FAX_DIRECTOR_PATH, self.FAX_DIRECTOR_PATH)
        
        
    def _handler_btn_file_move_all(self):     
        pass
        # directory_name.FileMove(self, self.selected_file_from_Listbox )



class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Replace')
        self.geometry('500x500+2000+100')
        # layout on the root window
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):

        fax_receive = GUI_FaxReceive(self)
        # fax_receive.grid(column=0, row=1)



if __name__ == "__main__":
    app = App()
    app.mainloop()        