import os
import glob
import time

    
class FaxReceive():
    def __init__(self,dir_path):
        
        self.DIRECTOR_PATH = dir_path
        self.selected_file =''
        # self.src_path = self.DIRECTOR_PATH
    
    def __get_directory_file(self):
        return  glob.glob(self.DIRECTOR_PATH +'/*.*')
        # return  [file for file in load_files if file.endswith('.jpg')]
    
    def __get_sorted_faxfiles(self,file_list):
        checked_list = []
        unchecked_list = [] 
        
        file_list.sort(key=os.path.getmtime)

        for f in file_list:
            if os.path.basename(f)[0] == 'v':
                checked_list.append(f)
            else :
                unchecked_list.append(f)
        return unchecked_list, checked_list
    
    def get_faxfiles(self):
        return self.__get_sorted_faxfiles(self.__get_directory_file())     
    
    
    def Rename_file(self, src_file, dst_name):
        if os.path.isfile(src_file):
        
            file_ext = os.path.splitext(src_file)[1] 
            file_ctime = time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(src_file)))
            dst_file_name = f'{self.DIRECTOR_PATH}{dst_name}_{file_ctime}{file_ext}'
            print(f'src_file : {src_file}')
            print(f'dst_file : {dst_file_name}')
            os.rename(src_file, dst_file_name)
                    
        else :
            print(f'Rename_file error : {src_file} is not found')
    
    def Delete_file(self, src_file):
        print(f'Delete_file={src_file}')
        
        if os.path.isfile(src_file):
            os.remove(src_file)
        else : 
            print(f"Delete_file error : {src_file} is not found")
        
   
    # def event_handler(self):
    #     print('event_handler')

    # def check_v_file(self,filename):
    #     self.company_name.delete(0,'end')
    #     self.company_name.insert(0,filename.split('_')[0])  
    #     # self.txt_value_entry = 'hello'

    #     if filename[0] == 'v' :
    #         self.chk_active.set(True)
    #         return True
    #     else :
    #         self.chk_active.set(False)
    #         return False

    # def items_selected(self,event):
    #     if not event.widget.curselection():
    #         return
    #     selected_indices = self.listbox.curselection()[0]
    #     self.src_file = self.listbox.get(selected_indices)
    #     self.check_v_file(os.path.basename(self.src_file))

    #     print(self.src_file)
        # print(selected_indices)
        # if selected_indices:
        #     # index = selected_indices[0]
        #     self.src_file = self.listbox.get(selected_indices)
        #     self.reload_file(os.path.basename(self.src_file))
        #     # self.company_name.select_adjust(tkinter.END)
        # else:
        #     print("No entry") 
    

    # def items_doubleClicked(self,event):
    #     if not event.widget.curselection():
    #         return
    #     selected_indices = self.listbox.curselection()[0]
    #     self.src_file = self.listbox.get(selected_indices)
    #     subprocess.Popen(f'c:/imagine/imagine64.exe {self.src_file}')

        # selected_indices = self.listbox.curselection()
        # msg = self.listbox.get(selected_indices[0])
        # os.system(f'./img/{msg}')



    # def FAX_rename(self, dst_file, is_checked) :
        
    #         try :
    #             # creation_time = time.gmtime(os.path.getctime(self.src_file))
    #             file_ctime = time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(self.src_file)))

    #             file_path, file_name_ext = os.path.split(self.src_file)
    #             file_name , file_ext = os.path.splitext(file_name_ext)

    #             if is_checked :
    #                 dst_file_name = f'v_{dst_file}'
    #             else : 
    #                 dst_file_name = dst_file.lstrip('v_')
                
    #             try :
    #                 dst_file_name = f'{file_path}/{dst_file_name}_{file_ctime}{file_ext}'
    #                 os.rename(self.src_file,dst_file_name)
    #                 self.noCheck_files()
    #             except FileExistsError :
    #                 print(f'{dst_file_name} is exited')
    #         except FileNotFoundError :
    #             print(f'{self.src_file} is not found')

    

    # def all_files(self):
    #     self.listbox['listvariable'] = Variable(value=self.get_file())

    # def noCheck_files(self):
    #     noChk_file_list = [file for file in self.get_file() if os.path.basename(file)[0] != 'v']
    #     self.listbox['listvariable'] = Variable(value=noChk_file_list)

    # def checked_files(self):
    #     noChk_file_list = [file for file in self.get_file() if os.path.basename(file)[0] == 'v']
    #     self.listbox['listvariable'] = Variable(value=noChk_file_list)

    # def convert_filename(self):
    #     self.FAX_rename( self.company_name.get(), self.chk_active.get())

    # def handle_watchdog_event(self, event):
    #     """Called when watchdog posts an event"""
    #     watchdog_event = self.queue.get()
    #     print("event type:", watchdog_event)

    # def shutdown(self, event):
    #     print("""Perform safe shutdown when GUI has been destroyed""")
    #     self.observer.stop()
    #     self.observer.join()

    # def notify(self, event):
    #     """Forward events from watchdog to GUI"""
    #     self.queue.put(event)
    #     self.handle_watchdog_event(event)
