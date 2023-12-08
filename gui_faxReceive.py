
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
        
        
        self.file_listbox = Listbox(self, width=50,selectmode=SINGLE) 
        self.file_listbox.grid(row=0,column=0) 
        
        self.btn_frame = Frame(self)
        self.refile_name = Entry(self.btn_frame,width=15).grid(row=0 ,column=0, padx=10 )
        # Checkbutton(self.btn_frame,width=10,  text="Checked").grid(row=0 ,column=1) 
        Button(self.btn_frame,width=10, text="RE:name").grid(row=0 ,column=2) 
        Button(self.btn_frame,width=10,  text="delete").grid(row=0 ,column=3) 
        self.btn_frame.grid(row=1,column=0)
        
        self.FAX_R.get_directory_file(self)
    
    
    def __set_listbox_data(self, data_list):
        # for i 
        self.file_listbox.insert()
        # self.all_files()
        
    # def remove_item(self): 
    #     selected_checkboxs = self.file_listbox.curselection() 
    
    #     for selected_checkbox in selected_checkboxs[::-1]: 
    #         self.file_listbox.delete(selected_checkbox) 

    # def get_file(self):    
    #     load_files = glob.glob(DIRECTOR_PATH +'/*.*')
    #     return  [file for file in load_files if file.endswith('.jpg')]

    # def all_files(self):
    #     self.file_listbox['listvariable'] = Variable(value=self.get_file())


    
  

















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