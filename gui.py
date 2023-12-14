import tkinter as tk
from tkinter import ttk
import gui_pdf2jpg
import gui_faxReceive
import gui_calculator


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('OCprogram')
        self.geometry('500x500+2000+100')
        
        # ico = tk.PhotoImage(file='./peach.png')
        # self.iconphoto(default=False, ico)   
        # self.iconphoto(default=False, tk.PhotoImage(file='./peach.png'))   
        # self.resizable(0, 0)
        # windows only (remove the minimize/maximize button)
        # self.attributes('-toolwindow', True)

        """layout on the root window""" 
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        # create the input frame
        input_frame = gui_pdf2jpg.Pdf2jpg(self,8)
        input_frame.grid(column=0, row=0, pady = 20)
        fax_receive = gui_faxReceive.GUI_FaxReceive(self)
        fax_receive.grid(column=0, row=1, pady = 20)
        calc = gui_calculator.Calculator(self)
        calc.grid(column=0, row=2)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()