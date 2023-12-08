import menu_PDF2Jpg_Convertor
import menu_FAX
import tkinter


FAX_DIR = './fax_receive'
PDF_SRC_DIR_PATH = 'C:/Users/kindk/Downloads'
PDF_TO_JPG_DEST_DIR_PATH = 'C:/Users/kindk/dst'

root = tkinter.Tk()


root.title("OC PROGRAMS")
app1 = menu_PDF2Jpg_Convertor.PDFconvert(root, PDF_SRC_DIR_PATH, PDF_TO_JPG_DEST_DIR_PATH)
app1.grid(row=0, column=0)

app2 = menu_FAX.MenuFax(root, FAX_DIR )
app2.grid(row=1, column=0)
btn_close = tkinter.Button(root, padx=5, pady=5, text="Close", width=12, command=root.quit)
btn_close.grid(row=2)



root.resizable(True, True)
root.geometry("600x600+100+10")
root.mainloop()
