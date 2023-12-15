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
        gui_pdf2jpg.Pdf2jpg(self, 0, 0, 8)
        
        gui_faxReceive.GUI_FaxReceive(self, 1, 0 )
        
        gui_calculator.Calculator(self, 2, 0)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()