import tkinter as tk

def add_row():
    new_row = []
    for j in range(5):
        entry = tk.Entry(root)
        entry.grid(row=len(entry_list), column=j, padx=5, pady=5)
        new_row.append(entry)
    entry_list.append(new_row)

def remove_row():
    if entry_list:
        row_to_remove = entry_list.pop()
        for entry in row_to_remove:
            entry.destroy()

root = tk.Tk()
root.title("Row 추가/삭제 예제")

entry_list = []

# 초기에 5x5의 Entry 위젯 생성
for i in range(5):
    row = []
    for j in range(5):
        entry = tk.Entry(root)
        entry.grid(row=i, column=j, padx=5, pady=5)
        row.append(entry)
    entry_list.append(row)

# + 버튼 생성 및 클릭 시 add_row 함수 호출
add_button = tk.Button(root, text="+", command=add_row)
add_button.grid(row=5, column=0, pady=5)

# - 버튼 생성 및 클릭 시 remove_row 함수 호출
remove_button = tk.Button(root, text="-", command=remove_row)
remove_button.grid(row=5, column=1, pady=5)

root.mainloop()
