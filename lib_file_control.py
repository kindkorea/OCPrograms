import os
import datetime
import subprocess
from ConfigControlFile import ConfigureIni
import shutil
class FaxFileControl():
    
    def __init__(self):
        self.extension_viewer = ConfigureIni.read('fax','extension_viewer')
        self.fax_trash_bin_folder = ConfigureIni.read('fax','fax_trash_bin_folder')
        # print(self.extension_viewer)
        
    def _get_file_path_in_folder(self, file_path):
        try:
            # 주어진 디렉토리에서 파일만 가져옵니다.
            file_list = [os.path.join(file_path, file) for file in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, file))]
            
            # 파일들을 수정 시간 순서대로 정렬합니다.
            sorted_file_list = sorted(file_list, key=os.path.getmtime)
            
            return sorted_file_list
        except FileNotFoundError:
            print("디렉토리를 찾을 수 없습니다. 올바른 경로를 입력해 주세요.")
            return []
        except Exception as e:
            print(f"에러가 발생했습니다: {e}")
            return []
        
    def _get_file_name(self, list):
        try:
            # 파일 경로에서 파일명만 추출하여 리스트로 반환합니다.
            file_names = [os.path.basename(file) for file in list]
            return file_names
        except Exception as e:
            print(f"에러가 발생했습니다: {e}")
            return []

    
    def _separate_v_file(self, file_list):
        list_v = []
        list_non_v = []

        for item in file_list:
            if item[0:3] == '[v]':
                list_v.append(item)
            else:
                list_non_v.append(item)
        # print(f'{list_v=}')
        # print(f'{list_non_v=}')
        return list_v, list_non_v
    
    def run_with_viewer(self,file_path, src_file):
        """
        src_file 을 확장 jpg뷰어로 실행함
        Args:
            file_path
            src_file
        
        Returns:
        
        """
        try : 
            file_path = os.path.join(file_path,src_file)
            
            # cmd = f'{self.extension_viewer} {file_path}'
            # subprocess.Popen(cmd)
            os.startfile(file_path)
        
        except FileNotFoundError :
            print(f'Error: The file {src_file} does not exist.')
            
            
    def checking_v_file(self, filepath, src_filename):
        """
        src_filename에 [v] 확인 도장을 찍거나 삭제함
        
        Args: 
        filepath : 해당 파일의 경로
        src_filename : 해당 파일 이름
        
        Returns:
        성공하면 변경된 파일을 리턴함
        """

        try:
            # 파일 이름이 [v]로 시작하는지 확인합니다.
            if src_filename[:3] == '[v]':
                # [v]를 제거한 새 파일 이름 생성
                new_filename = src_filename[3:]
            else:
                # [v]를 추가한 새 파일 이름 생성
                new_filename = '[v]' + src_filename
            
            # 새 파일 경로 생성
            src_full_path = os.path.join(filepath, src_filename)
            new_full_path = os.path.join(filepath, new_filename)
            
            os.rename(src_full_path , new_full_path)
            return new_full_path
        except Exception as e:
            print(f"에러가 발생했습니다: {e}")
            return None
        
    def delete_file(self, filepath, src_filename):
        """
        src_filename 을 삭제
        
        Args: 
        filepath : 해당 파일의 경로
        src_filename : 삭제할할 파일 이름
        
        Returns:
        """
        try :
            src_file_path = os.path.join(filepath,src_filename)
            if os.path.isfile(src_file_path):
                try : 
                    # send2trash.send2trash(src_file_path)
                    shutil.move(src_file_path, self.fax_trash_bin_folder)
                except Exception as err :
                    print(f'send2trash occur exception {err}')
        except FileNotFoundError :
            print(f'Error: The file {src_file_path} does not exist.')
        # try:
        #     # 삭제할 파일의 전체 경로를 생성합니다.
        #     file_path = os.path.join(filepath, src_filename)

        #     # 파일이 존재하는지 확인하고 삭제합니다.
        #     if os.path.isfile(file_path):
        #         os.remove(file_path)
        #         print(f"파일 '{src_filename}'이 성공적으로 삭제되었습니다.")
        #     else:
        #         print(f"파일 '{src_filename}'을 찾을 수 없습니다.")
        # except Exception as e:
        #     print(f"파일 삭제 중 에러가 발생했습니다: {e}")

    
    def rename_fax_file_with_date(self, filepath, src_filename , dst_filename ):
        
        """
        src_filename 을 dst_filename_년-월-일.확장자 로 변경
        
        Args: 
        filepath : 해당 파일의 경로
        src_filename : 변경할 파일 이름
        dst_filename : 변경될 이름
        
        Returns:
             성공시 변경된 파일을 리턴함
                예) 'test.py'을 '안녕_2024-11-13' 
        """
        
        try:
            # 파일의 전체 경로를 생성합니다.
            src_full_path = os.path.join(filepath, src_filename)
            
            # 파일 생성 시간을 가져옵니다.
            creation_time = os.path.getctime(src_full_path)
            creation_date = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
            _, file_extension = os.path.splitext(src_filename)
            # 새로운 파일명 생성
            new_filename = f"{dst_filename}_{creation_date}"
            new_full_path = ''
            new_full_filename = f"{dst_filename}_{creation_date}{file_extension}"
            new_full_path = os.path.join(filepath, new_full_filename)
            count = 1
            while os.path.exists(new_full_path):
                new_full_filename = f'{new_filename}#{count}{file_extension}'
                new_full_path = os.path.join(filepath, new_full_filename)
                count += 1
           
            # 파일 이름을 변경합니다.
            os.rename(src_full_path, new_full_path)

            print(f"파일이 '{src_filename}'에서 '{new_filename}'으로 성공적으로 변경되었습니다.")
            return new_filename
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다. 올바른 경로를 입력해 주세요.")
            return None
        except Exception as e:
            print(f"에러가 발생했습니다: {e}")
            return None


    
    def get_sorted_filename(self, folder_path):
        return self._get_file_name(self._get_file_path_in_folder(folder_path))
    
    def get_fax_file(self, folder_path): 
        """
        팩스 수신 폴더를 GUI단 데이터 리턴함

        Args:
            
        Returns:
            [v]유무 v_list, non_v_list 두가지 리스트를 리턴함
        """
        return self._separate_v_file(self.get_sorted_filename(folder_path))
        
    def get_sorted_filename(self, folder_path):
        """
        팩스 수신 폴더를 GUI단 데이터 리턴함

        Args:
            folder_path : 소스 폴더명
            
        Returns:
            folder_path 의 폴더에 모든 파일명만 시간순서로 리턴함
        """
        return self._get_file_name(self._get_file_path_in_folder(folder_path))
        

    
if __name__ == '__main__':
    a = FaxFileControl()
    