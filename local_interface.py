#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 13:43:27 2024

@author: quentin
"""




import tkinter as tk
from tkinter import ttk
import pandas as pd

class DataFrameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DataFrame Interface")
        
        self.data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'Los Angeles', 'Chicago']
        }
        self.df = pd.DataFrame(self.data)

        self.tree = ttk.Treeview(root, columns=list(self.df.columns), show='headings')
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for index, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))

        self.tree.pack(expand=True, fill='both')

if __name__ == "__main__":
    root = tk.Tk()
    app = DataFrameApp(root)
    root.mainloop()