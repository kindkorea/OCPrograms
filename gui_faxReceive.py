
from tkinter import *
import os
import glob
import lib_faxReceive
  
  
DIRECTOR_PATH = 'C:/Users/kindk/.vscode/test/'
# Function will remove selected Listbox items 



class GUI_FaxReceive(Frame):
    def __init__(self, container):
        super().__init__(container)
        # self.file_listbox
        self.__create_widgets()
        
    def __create_widgets(self):
        
        self.FAX_R = lib_faxReceive.FaxReceive(DIRECTOR_PATH)
        
        
        self.file_listbox = Listbox(self, width=50, selectmode=SINGLE) 
        self.file_listbox.grid(row=0,column=0) 
        self.file_listbox.bind("<Key>",self.__handler_key)
        self.file_listbox.bind("<Double-Button-1>",self.__handler_mouse)
        
        self.btn_frame = Frame(self)
        self.refile_name = Entry(self.btn_frame,width=15)
        self.refile_name.grid(row=0 ,column=0, padx=10 )
        # Checkbutton(self.btn_frame,width=10,  text="Checked").grid(row=0 ,column=1) 
        Button(self.btn_frame,width=10, text="RE:name" , command=self.__func_rename).grid(row=0 ,column=2) 
        Button(self.btn_frame,width=10,  text="delete" , command=self.__func_delete).grid(row=0 ,column=3) 
        self.btn_frame.grid(row=1,column=0)
        self.__reset_listbox()
    
    def __handler_key(self, event):
        
        code = event.keycode
        print(code)
        if code == 46:  #key : del
            # print("function : rename")
            self.__func_delete()
        elif code == 113: #key : F2
            self.__func_rename()
        elif code == 13: #key : enter
            self.__run_with_viewer(self.__selected_src_file())
        # elif code == 38:  #key : up
        #     print('up')     
        # elif code == 40:  #key : down
        #     print('down')     

    def __handler_mouse(self,event):
        if not event.widget.curselection():
            return
        self.__run_with_viewer(self.__selected_src_file())
        
        
    def __reset_listbox(self):
        unchecked, checked = self.FAX_R.get_faxfiles()
        self.__set_listbox_data(unchecked,checked)
    
    def __set_listbox_data(self, unchecked_files, checked_files):
        self.file_listbox.delete(0,END)
        for f in checked_files:
            self.file_listbox.insert(0,f)
            
        for f in unchecked_files:
            self.file_listbox.insert(0,f)
        
        for i in range(len(checked_files)):
            self.file_listbox.itemconfig(len(unchecked_files)+i, {'fg':'gray'})
        
    def __func_delete(self):
        self.FAX_R.Delete_file(self.__selected_src_file())
        self.__reset_listbox()
        
    def __selected_src_file(self):
        index = self.file_listbox.curselection()[0]
        if index : # if the tuple is not empty
            return self.file_listbox.get()  
        
    
    def __func_rename(self):
        print('__func_rename')
        src_file = self.__selected_src_file()
        dst_filename = self.refile_name.get()
        self.FAX_R.Rename_file( src_file, dst_filename)
        self.__reset_listbox()


    def __run_with_viewer(self, src_file):
        print(f'__run_with_viewer = {src_file}')
  

















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
        fax_receive = GUI_FaxReceive(self)
        fax_receive.grid(column=0, row=1)
        # # create the button frame
        # button_frame = gui_pdf2jpg.Cb_Btn_frame(self,8)
        # button_frame.grid(column=0, row=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()        