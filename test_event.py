import tkinter as tk
from tkinter import ttk

class NumberEntryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Number Entry")
        self.geometry("300x100")

        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Enter Number:")
        label.grid(row=0, column=0, padx=10, pady=10)

        self.number_entry = ttk.Entry(self)
        self.number_entry.grid(row=0, column=1, padx=10, pady=10)

        convert_button = tk.Button(self, text="Convert", command=self.convert_number)
        convert_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=2, column=0, columnspan=2, pady=10)

    def convert_number(self):
        try:
            entered_number = int(self.number_entry.get())
            formatted_number = '{:,}'.format(entered_number)  # 천 단위로 구분
            self.result_label.config(text=f"Formatted Number: {formatted_number}")
        except ValueError:
            self.result_label.config(text="Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    app = NumberEntryApp()
    app.mainloop()
