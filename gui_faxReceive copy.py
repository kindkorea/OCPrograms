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

import settingFille
import lib_file_control 
# from settingFille import ConfigureIni

class CustomHandler(FileSystemEventHandler):
    def __init__(self, app):
        FileSystemEventHandler.__init__(self)
        self.app = app
    def on_created(self, event):     
        self.app.notify_creation(event)
        
    def on_deleted(self, event): self.app.notify(event)
    def on_modified(self, event): self.app.notify(event)
    def on_moved(self, event): self.app.notify(event)

# class CompanyButtonApp:
#     def __init__(self, root , callback):
#         self.root = root
#         # self.root.title("Grid Button App")
#         self.companies =  ConfigureIni.read_and_return_list('fax','companies_name')
#         self.companies_bookmarked =  ConfigureIni.read_and_return_list('fax','companies_name_bookmarked')
        
#         self.companies.sort()
#         self.callback = callback
#         self.create_buttons()
        

#     def create_buttons(self):
#         for index, title in enumerate(self.companies):
#             row = index // 6
#             column = index % 6
#             button = Button(self.root, text=title, command=lambda x=title: self.callback(x))
#             button.grid(row=row, column=column, padx=5, pady=5 , sticky='ew')


                        
# class ChangeNameValue:
#     def __init__(self):
#         self.changing_name = ''
    
#     @property
#     def name(self):
#         return self.changing_name
#     @name.setter
#     def name(self, value):
#         self.changing_name = value
        
        
    
        
class GUI_FaxReceive():
    def __init__(self, containerFrame):
        
        self.container = containerFrame
        
        # self.companies = [
        #     "한국산업",
        #     "건한",
        #     "나산팀버",
        #     "대한테이프",
        #     "단가표",
        #     "두산종합목재",
        #     "삼원목재",
        #     "에스디팀버",
        #     "온보드",
        #     "우진프레임",
        #     "원스탑우드",
        #     "진양",
        #     "케이디우드",
        #     "크나우프",
        #     "태진목재",
        #     "사업자",
        #     "기타",
        #     "경비_주유소",
        #     "경비_경동화물",
        #     "경비_대신화물"
            
        # ]
        self.companies = settingFille.JsonReader.read('companies_name.json')['companies_name']
        self.bookmarked_companies = settingFille.JsonReader.read('companies_name.json')['bookmarked_companies_name']
        
        self.selected_files = []
        self.fax_root_folder = settingFille.ConfigureIni.read('fax','fax_save_folder')
        self.fax_archive_folder = settingFille.ConfigureIni.read('fax','archive_folder')
        # self.extension_viewer = ConfigureIni.read('fax','extension_viewer')
        self.fax_control = lib_file_control.FaxFileControl()
        self.frame_main = LabelFrame(self.container, text='팩스 수신')
        self.frame_main.grid(row=0,column=0, padx=2 ,pady = 2)
        self._create_widgets()
        # self.selected_file_from_Listbox = list()
        
    
    def _create_widgets(self):
        """
        팩스 프로그램 GUI widget 생성
        
        Args: 

        Returns:
        """
        #left 프레임
        self.frame_left = Frame(self.frame_main)
        self.frame_left.grid(row=0,column=0, padx=2 ,pady = 2, sticky='ewns')
        
        # 팩스 리시브 폴더 로드                
        # self.FAX_R = lib_faxReceive.FaxReceive(ConfigureIni.read('fax','fax_save_folder'))  
        
        # 팩스 리시프 리스트 박스
        self.file_listbox = Listbox(self.frame_left, width=50,  height=25, selectmode=EXTENDED, highlightthickness=1) 
        self.file_listbox.grid(row=0, column=0, padx=5 ,pady=5 ,rowspan=4) 
        self.scrollbar=Scrollbar(self.frame_left, orient='vertical' ,command=self.file_listbox.yview)
        self.scrollbar.grid(row=0, column=1 , rowspan= 5, sticky='ns')
        self.file_listbox.config(yscrollcommand = self.scrollbar.set)
        self.file_listbox.bind("<Key>",self._handler_bind_key_from_file_listbox)
        self.file_listbox.bind("<Double-Button-1>",self._handler_doubleClick_from_file_listbox)
        
        # right 프레임
        self.frame_right = Frame(self.frame_main)
        self.frame_right.grid(row=0,column=1, pady = 2 ,sticky='ewns')
        
        # 왼쪽 버튼
        Button(self.frame_right, width=13,  height=3, text="리로드" , command=self._refresh_listbox).grid(row=0 ,column=2,  padx= 10 ,pady= 2 ,sticky='nsew')
        Button(self.frame_right, width=13,  height=3, text="열기(ENTER)" , command=self._run_with_viewer).grid(row=1 ,column=2,  padx= 10 ,pady= 2,sticky='nsew')
        Button(self.frame_right, width=13,  height=3, text="이름변경(F2)" , command=self._handler_btn_rename).grid(row=2,column=2, padx= 10 ,pady= 2,sticky='nsew') 
        Button(self.frame_right, width=13,  height=3, text="체크함" , command=self._handler_btn_v_check).grid(row=3 ,column=2,  padx= 10 ,pady= 2,sticky='nsew') 
        Button(self.frame_right, width=13,  height=3, text="삭제(DEL)" , command=self._handler_btn_delete).grid(row=4 ,column=2,padx= 10 ,pady= 2,sticky='nsew')
        
        
        
        #mid 프레임
        self.frame_mid = Frame(self.frame_main)
        self.frame_mid.grid(row=1,column=0, columnspan=3, padx=10 ,pady = 10,sticky='ewns')
    
        
        # 이름변경 엔트리
        self.entry_changingName = Entry(self.frame_mid)
        self.entry_changingName.bind("<Return>",self._handlr_bind_rename)
        # self.entry_changingName.bind("<Button-1>", self._select_all_text)
        self.entry_changingName.grid(row=0, column=0, columnspan= 2, sticky='EW')

        # 라디오 버튼 생성
        self.radio_var = StringVar()
        self.radio_var.set("comp_name")  # 기본값 설정
        self.radio_btn_name = Radiobutton(self.frame_mid, text="팩스 이름", variable=self.radio_var, value="comp_name")
        self.radio_btn_open_folder = Radiobutton(self.frame_mid, text="팩스 찾기", variable=self.radio_var, value="open_folder")
        self.radio_btn_name.grid(row=0 , column=4 , sticky="ew")
        self.radio_btn_open_folder.grid(row=0 , column=5, sticky="ew")
        
        
        # bottom 프레임
        self.frame_bottom = Frame(self.frame_main )
        self.frame_bottom.grid(row=2,column=0, columnspan=6, padx=10 ,pady = 10,sticky='ewns')
        
        self.frame_bottom_bookmarked_companies= Frame(self.frame_bottom )
        self.frame_bottom_bookmarked_companies.grid(row=0,column=0, columnspan=6 ,padx=10 ,pady = 10, ipadx=10, ipady=5 ,sticky='ewns')
        
        self.frame_bottom_companies = Frame(self.frame_bottom )
        self.frame_bottom_companies.grid(row=1,column=0, columnspan=6 ,padx=10 ,pady = 10,sticky='ewns')
        
        
        Button(self.frame_bottom, width=13,   text="즐겨찾기" , command=self._handler_btn_companies_bookmark).grid(row=3 ,column=0, padx= 10 ,pady= 2,sticky='nsew')
        Button(self.frame_bottom, width=13,   text="회사등록" , command=self._handler_btn_companies_add).grid(row=3 ,column=1, padx= 10 ,pady= 2,sticky='nsew')
        Button(self.frame_bottom, width=13,   text="모든파일이동" , command=self._handler_btn_file_move).grid(row=3 ,column=3, padx= 10 ,pady= 2,sticky='nsew')
        self.to_change_company_name = StringVar()
        
        
        self._refresh_listbox()
        self._make_widget_bottom_buttons()
        
    
    
    def _handler_bottom_btn(self, txt):
        """
        하단 버튼의 이벤트 핸들러
        
        Args: 
        txt : 버튼의 값
        
        Returns:
        """
        self.entry_changingName.delete(0,END)
        self.entry_changingName.insert(0,f'{txt}_')
        self.entry_changingName.focus_set()
        self.entry_changingName.icursor(END)
        # print(f'{txt}버튼이 눌렸습니다.')     
    
    # 하부 회사 버튼 만들기
    def _make_widget_bottom_buttons(self):
        for ix, txt in enumerate(self.bookmarked_companies):
            self._make_bottom_button(self.frame_bottom_bookmarked_companies, ix//6, ix%6 ,txt)
            
        for ix, txt in enumerate(self.companies):
            self._make_bottom_button(self.frame_bottom_companies, ix//6, ix%6 ,txt)
            
            
    # 하단 버튼 생성 함수   
    def _make_bottom_button(self, f, row, col , text):
        _b = Button(f, text=text, width=10 ,  command=lambda x = text :self._handler_bottom_btn(x))
        _b.grid(row=row, column=col , sticky='ew')  # 버튼을 그리드의 두 번째 행과 첫 번째 열에 배치
        
        
    # 리스트 박스 더블 클릭시 bind 함수   
    def _handler_doubleClick_from_file_listbox(self,e):
        self._run_with_viewer()
    

    def _run_with_viewer(self):  
        """
        선택된 파일을 외부 뷰어로 실행함
        
        Args: 
        
        Returns:
        """
        selected_file = self._get_selected_files_from_listbox()
        if  selected_file : 
            for src_name in selected_file:
                # self.FAX_R.run_with_viewer(src_name)
                self.fax_control.run_with_viewer(self.fax_root_folder,  src_name)
        else :
            print('self.selected_file_from_Listbox is empty')
        
    def _refresh_listbox(self):
        """
        팩스 폴더 파일로 리스트 박스 갱신함
        
        Args: 
        
        Returns:
        """
        self.file_listbox.delete(0,END)
        v_checked , non_v_list  = self.fax_control.get_fax_file(self.fax_root_folder)
        self._setting_list_in_listbox(v_checked, True)
        self._setting_list_in_listbox(non_v_list, False)
        
    def _setting_list_in_listbox(self, file_list , state):
        """
        리스트 아이템 글자 색을 변경함
        ([v] 있으면 그레이)
        Args: 
        
        Returns:
        """
        
        for f in file_list:
            self.file_listbox.insert(0,f)
        if state :
            for i in range(len(file_list)):
                self.file_listbox.itemconfig(i, {'fg':'gray'})
    
    
    # """Forward events from watchdog to GUI"""
    # def notify_creation(self,event):
    #     print(f'file created{event.src_path}' )
        

    
    # def notify(self, event):
    #     self.queue.put(event)
    #     self._refresh_listbox()      
    
    def _handler_bind_key_from_file_listbox(self, event):
        
        code = event.keycode
        # print(code)
        if code == 46:  #key : del
            self._handler_btn_delete()
            
        elif code == 113: #key : F2
            # self.entry_changingName.focus_set()
            self._handler_btn_rename()
            
            
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
        
    def _get_selected_files_from_listbox(self):
        """
        리스트 박스에서 선택된 파일을 리스트로 반환함
        
        Args: 
        
        Returns:
            선택된 파일을 반환함
        """
        
        selected_indices = self.file_listbox.curselection()
        if selected_indices :
            return [self.file_listbox.get(idx) for idx in selected_indices]
        
        
    def _handler_btn_rename(self):  # 이름변경 버튼
        """
        선택된 파일의 이름을 변경함
        
        Args: 
        
        Returns:
            
        """
        nameEntry = self.entry_changingName.get()
        if nameEntry : 
             self._rename(nameEntry)
        else : 
            self.entry_changingName.focus()
            # self.entry_changingName.insert(0, "변경할 이름을 입력하세요.")

    
    # def _rename_faxFile(self, dst_name):
    #     nameEntry = self.entry_changingName.get()
    #     if nameEntry != '' : 
    #         self._rename(dst_name + '_' + nameEntry )
    #     else : 
    #         self._rename(dst_name)
            
            
    def _open_faxFile(self,dst_name):
        import lib_move_file
        a = lib_move_file.MoveFaxFile()
        
        # filename = dst_name
        file_path = a.search_folder_by_keyword(dst_name)
        if file_path:
            file_list = self.FAX_R.get_file_from_folder(file_path)
            self._set_list_to_listbox(file_list,True)
            # print(f"open {file_list}")
        
    # def _callback_company_name(self, dst_name):  #하단의 상호명 버튼
    #     selected_value = self.radio_var.get()
    #     if selected_value == 'comp_name' :
    #         self._rename_faxFile(dst_name)
            
    #     elif selected_value == 'open_folder' :
    #         self._open_faxFile(dst_name)
        
    
        
    def _handlr_bind_rename(self, e): #entry bind handler
        """
        파일의 변경할 이름의 엔트리의 이벤트 핸들러
            엔트리의 값이 있으면 이름 변경
        Args: 
        
        Returns:
            
        """
        nameEntry = self.entry_changingName.get()
        if nameEntry != '' : 
             self._rename(nameEntry)
        else : 
            pass
    
    def _rename(self,dst_name : str):
        """
        이름을 변경하는 함수
        Args: 
        dst_name 변경할 텍스트 값
        
        Returns:
            
        """
        selected_files = self._get_selected_files_from_listbox()

        if dst_name != '' and selected_files : 
            for f_name in selected_files:
                self.fax_control.rename_fax_file_with_date(self.fax_root_folder , f_name, dst_name)
            self._refresh_listbox()
            self.entry_changingName.delete(0,END)  
        else :
            print('put changing name in entry')
            
        pass        
       
    
        
    def _handler_btn_v_check(self):
        """
        파일이름 앞에 [v] 을 붙이고 제거하고 토글함
        
        Args: 
        
        Returns:
        """
        selected_file = self._get_selected_files_from_listbox()
        if  selected_file : 
            for src_name in selected_file:
                self.fax_control.checking_v_file(self.fax_root_folder, src_name)
                # self.FAX_R.is_checked(src_name)           
            self._refresh_listbox()
        else :
            print('self.selected_file_from_Listbox is empty')    
    
         
    def _handler_btn_delete(self):
        """
        선택된 파일을 삭제함
        (사실상 특정폴더로 옮김)
        Args: 
        
        Returns:
        """
        selected_file = self._get_selected_files_from_listbox()
        if  selected_file : 
            for src_name in selected_file:
                if messagebox.askyesno('파일삭제', 
                                       f'{src_name}을 삭제할까요?',
                                        # parent=self,
                                        # geometry="+{}+{}".format(self.winfo_x(), self.winfo_y()),
                                       ) :
                    self.fax_control.delete_file(self.fax_root_folder,src_name)   
            self._refresh_listbox()
        else :
            print('self.selected_file_from_Listbox is empty')

    
    
    def _handler_btn_companies_bookmark(self):
        """
        하단 버튼의 즐겨찾기 추가 // 삭제
        Args: 
        
        Returns:
        """
        pass
        
    def _handler_btn_companies_add(self):
        """
        하단 버튼의 회사 추가 // 삭제
        Args: 
        
        Returns:
        """
        pass
        
    def _handler_btn_file_move(self):
        """
        [v]가 있는 파일들만 해당 폴더(회사명)로 이동시킴
        (사실상 특정폴더로 옮김)
        Args: 
        
        Returns:
        """     
        import lib_move_file
        a = lib_move_file.MoveFaxFile()
        a.doMove()
        


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Replace')
        self.geometry('800x700+1500+100')
        # layout on the root window
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        fax_receive = GUI_FaxReceive(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()        