import tkinter as tk

class EntryGridApp(tk.Frame):
    def __init__(self, root, count_row, count_col, enter_handler):
        self.root = root
        self.root.title("Entry Grid Example")

        # 5x5 크기의 엔트리 그리드 생성
        self.entries = [[tk.Entry(root, width=5) for _ in range(5)] for _ in range(5)]
        self.current_row = 0
        self.current_column = 0

        # 엔트리 배치
        for row in range(5):
            for col in range(5):
                self.entries[row][col].grid(row=row, column=col, padx=5, pady=5)

        # 방향키 이벤트 바인딩
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)

    def move_left(self, event):
        self.move(-1, 0)

    def move_right(self, event):
        self.move(1, 0)

    def move_up(self, event):
        self.move(0, -1)

    def move_down(self, event):
        self.move(0, 1)

    def move(self, dx, dy):
        # 현재 위치에서 이동한 새 위치 계산
        new_row = (self.current_row + dy) % 5
        new_col = (self.current_column + dx) % 5

        # 현재 위치의 엔트리에서 포커스 제거
        self.entries[self.current_row][self.current_column].focus_set()

        # 새 위치의 엔트리에 포커스 설정
        self.entries[new_row][new_col].focus_set()

        # 현재 위치 갱신
        self.current_row = new_row
        self.current_column = new_col

# Tkinter 윈도우 생성
root = tk.Tk()

# 애플리케이션 인스턴스 생성
app = EntryGridApp(root)

# 윈도우 실행
root.mainloop()
