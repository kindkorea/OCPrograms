import tkinter as tk

class SpreadsheetApp(tk.Frame):
    def __init__(self, container, rows, columns):
        super().__init__(container)
        # 데이터를 저장할 2차원 리스트
        self.data = [['' for _ in range(columns)] for _ in range(rows)]

        # Entry 위젯을 담을 2차원 리스트
        self.entries = [[None for _ in range(columns)] for _ in range(rows)]

        # 스프레드시트를 위한 프레임
        self.create_spreadsheet()

    def create_spreadsheet(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                # Entry 위젯 생성
                entry = tk.Entry(self, width=10)
                entry.grid(row=i, column=j)

                # 데이터와 Entry 위젯을 연결
                entry.insert(0, self.data[i][j])
                entry.bind('<FocusOut>', lambda e, i=i, j=j: self.update_cell(i, j))

                # Entry 위젯을 2차원 리스트에 저장
                self.entries[i][j] = entry

    def update_cell(self, row, col):
        # Entry 위젯의 값으로 데이터 업데이트
        new_value = self.entries[row][col].get()
        print(new_value)
        self.data[row][col] = new_value
        # print(self.data)




class mySheet(SpreadsheetApp):
    def __init__(self, container, rows, columns, hsadfsd):
        super().__init__(container, rows, columns)
        self.h = hsadfsd
        
        
    def create_spreadsheet(self):
        
        for i in range(len(self.data)):
            tk.Button(self, text=f'{i}vat' , command=lambda x=i :self._handler_btn_vat(x)).grid(row=i,column=0)
            for j in range(len(self.data[0])):
                # Entry 위젯 생성
                j
                entry = tk.Entry(self, width=10)
                entry.grid(row=i, column=j+1)

                # 데이터와 Entry 위젯을 연결
                entry.insert(0, self.data[i][j])
                entry.bind('<FocusOut>', lambda e, i=i, j=j: self.update_cell(i, j))

                # Entry 위젯을 2차원 리스트에 저장
                self.entries[i][j] = entry
        
    def _handler_btn_vat(self,ix):
        print(f'{ix} pushed button')
        
        
    def update_cell(self, row, col):
        print('overloaded',self.h)
        


if __name__ == "__main__":
    root = tk.Tk()
    app = mySheet(root, rows =5, columns=5, hsadfsd='hi')
    app.grid(row=0, column=0)
    root.mainloop()
