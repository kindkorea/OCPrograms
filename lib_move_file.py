import os
import shutil
import subprocess
from settingFille import ConfigureIni


class LoggingMoveFile():
    
    @staticmethod
    def log_file(log_file_name ,log_file):
        with open(log_file_name, 'w', encoding='utf-8') as file:
            for item in log_file:
                file.write(item + '\n')
    @staticmethod                
    def open_logFile(log_file_name):
        try : 
            cmd = f'notepad {log_file_name}'
            subprocess.Popen(cmd)
        
        except FileNotFoundError :
            print(f'Error: The file {log_file_name} does not exist.')
        
    
        
class MoveFaxFile():
    
    def __init__(self):
        # self.log = LoggingMoveFile()
        self.src_folder = ConfigureIni.read('fax','fax_save_folder')
        self.dst_folder = ConfigureIni.read('fax','archive_folder')
    
 
    def _create_dst_folder_list(self):
        """기준 폴더 내 하위 폴더들을 읽어 딕셔너리로 반환하는 함수"""
        folder_list = {}
        
        # base_folder 내 모든 항목을 순회
        for folder_name in os.listdir(self.dst_folder):
            folder_full_path = os.path.join(self.dst_folder, folder_name)
            
            # 폴더만 처리
            if os.path.isdir(folder_full_path):
                folder_list[folder_name] = folder_full_path  # 폴더명 : 폴더경로
        
        return folder_list

    def _find_folder_by_key(self ,folder_list, src_key):
        """src_key를 포함한 폴더 이름에 해당하는 경로를 반환하는 함수"""
        # folder_list에서 키에 src_key가 포함된 폴더를 찾기
        for key, value in folder_list.items():
            if src_key in key:
                return value  # src_key를 포함한 폴더의 경로를 반환
        return None

    def _get_key_from_filename(self, filename):
        """ 파일명에서 키값을 추출함 
            [v] 에서 첫 _ 까지의 텍스트를 추출
            
            Args:
                filename 파일명
            
            Returns:
                seek_key 키값 < 이후 이값으로 해당 폴더를 검색함
        """
        if filename[0:3] == '[v]':
            # 첫 번째 '_' 전까지의 부분을 출력
            name_part = filename.split('_')[0]
            seek_key = name_part.split('[v]')[1]
            return seek_key
        
    def doMove(self):
        succeed_log = []
        failed_log = []
        folder_list = self._create_dst_folder_list()
        for filename in os.listdir(self.src_folder):
            src_key = self._get_key_from_filename(filename)
            if src_key:
                dst_folder = self._find_folder_by_key(folder_list , src_key)
                # print(f'{filename} > {dst_folder}')
                if dst_folder:
                    shutil.move(f'{self.src_folder}/{filename}', dst_folder)
                    succeed_log.append(f'SUCCESS : {filename}\t=>\t{dst_folder}')
                else : 
                    failed_log.append(f'FAILED : {filename} = \t\t dst folder')
            else :
                failed_log.append(f'FAILED : {filename} = \t\t KEY')
                
        # self.log.open_logFile()
        LoggingMoveFile.log_file('./log.txt', succeed_log + failed_log)
        LoggingMoveFile.open_logFile('./log.txt')
        

    def search_folder_by_keyword(self, keyword):
        """
        주어진 키워드로 1뎁스 폴더를 검색하여 경로를 반환합니다.

        Args:
            keyword (str): 검색할 키워드
            base_path (str): 검색할 기본 경로 (기본값은 현재 디렉토리)

        Returns:
            찾은 폴더 path 
        """
        try :
            for folder_name in os.listdir(self.dst_folder): 
                folder_path = os.path.join(self.dst_folder, folder_name)
                if os.path.isdir(folder_path) and keyword in folder_name:
                    return folder_path
        except : 
            return False

# 예제 사용
# search_and_open_folder("example_keyword", "C:/search_directory")
