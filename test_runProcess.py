import os

# 실행하려는 파일 경로
file_path = f'C:/Users/kindk/.vscode/OCPrograms/fax_receive/Travel_Photo.mp3'

# 파일 실행
try:
    os.startfile(file_path)
    print("파일 실행 성공")
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except OSError as e:
    print(f"오류 발생: {e}")
