
from tkinter import Tk, Listbox, Entry, StringVar, END, mainloop

import directory_name

def handler_key(e):
    key = e.keycode
    print(key)
    
    if key == 40 or key == 38 : # arrow up down
        listbox.focus()
    elif key == 13 or key == 32 : # enter and space
        cb_search()
    
    
def cb_search():
    sstr = search_str.get()
    listbox.delete(0, END)
    # If filter removed show all data
    if sstr == "":
        fill_listbox(main_data) 
        return
  
    filtered_data = list()
    for item in main_data:
        if item.find(sstr) >= 0:
            filtered_data.append(item)
   
    fill_listbox(filtered_data)   
  
def fill_listbox(ld):
    for item in ld:
        listbox.insert(END, item)
  
  
main_data = directory_name.forder_list.keys()
  
# GUI
master = Tk()
listbox = Listbox(master,selectmode = 'single')
listbox.pack()
fill_listbox(main_data)
  
search_str = StringVar()
search = Entry(master, textvariable=search_str, width=10 )
search.pack()
search.bind('<Key>', handler_key)
  
mainloop()