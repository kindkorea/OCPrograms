import tkinter as tk
from tkinter import ttk
from tkinter import * # __all__
import math
import directory_name as company
import os


class Calculator(Frame):
    def __init__(self, container):
        super().__init__(container)
        
        
        combo = ttk.Combobox(
        state="readonly",
        values=["Python", "C", "C++", "Java"]
        )
        combo.place(x=50, y=50)
        # button = ttk.Button(text="Display selection", command=display_selection)
        # button.place(x=50, y=100)

        
        for key in company.forder_list.keys(): 
            f = company.PATH + company.forder_list[key][1]
            print(f'{key} : {os.path.isdir(f)}')


    # def display_selection():
    #     # Get the selected value.
    #     selection = combo.get()
    #     messagebox.showinfo(
    #         message=f"The selected value is: {selection}",
    #         title="Selection"
    #     )    


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
        fax_receive = Calculator(self)
        fax_receive.grid(column=0, row=1)
        # # create the button frame
        # button_frame = gui_pdf2jpg.Cb_Btn_frame(self,8)

        
if __name__ == "__main__":
    app = App()
    app.mainloop()        
    
    