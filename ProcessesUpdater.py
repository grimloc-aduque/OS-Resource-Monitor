
import tkinter as tk
from tkinter import *

from DataSource import DataSource
from DataSourceProcesses import DataSourceProcesses
from Runnable import Runnable


class ProcessesUpdater(Runnable):

    frame:tk.Frame
    dataSource:DataSource
    labels:list[list[Label]]
    max_rows:int

    def __init__(self, frame:tk.Frame):
        super().__init__()
        self.frame = frame
        self.dataSource = DataSourceProcesses()
        self.max_rows = 19
        self.build_table()

    def build_table(self):
        self.dataSource.update_data()
        data = self.dataSource.get_data()
        columns = data.columns.to_numpy()
        for j in range(len(columns)):
            label = Label(self.frame, text=columns[j], font=('Arial', 14, 'bold'), padx=25)
            label.grid(row=0, column=j)

        self.labels = []
        for i in range(self.max_rows):
            row_labels = []
            for j in range(len(columns)):
                label = Label(self.frame, text='-', font=('Arial', 12), padx=25)
                label.grid(row=i+1, column=j)
                row_labels.append(label)
            self.labels.append(row_labels)

    def run_actions(self):
            self.dataSource.update_data()
            self.update_table()

    def update_table(self):
        data = self.dataSource.get_data()
        data = data.sort_values(by='Memory [GB]', ascending=False)
        data = data.head(self.max_rows).to_numpy()
        num_rows, num_cols = data.shape
        for i in range(num_rows):
            for j in range(num_cols):
                self.labels[i][j].config(text = data[i,j], font=('Arial', 12))
