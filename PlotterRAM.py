
import tkinter as tk

import numpy as np
from matplotlib.figure import Figure

from colors import colors
from DataSourceRAM import DataSourceRAM
from Plotter import Plotter


class PlotterRAM(Plotter):

    def __init__(self, frame:tk.Frame):
        super().__init__(frame)
        self.dataSource = DataSourceRAM()

    def generate_figure(self):
        return Figure(figsize=(6, 4), dpi=80)

    def plot(self):
        self._clean_figure()
        data = self.dataSource.get_data()

        subplot = self.figure.add_subplot(1, 2, 1)
        subplot.set_facecolor('none')
        cols_memory = ['Used Memory', 'Free Memory']
        data_memory = data[cols_memory]
        subplot.pie(data_memory, autopct= lambda val: np.round(val/100 * np.sum(data_memory), 2),
                           colors=[colors['orange'], colors['blue']])
        subplot.set_title("Memory Usage [GB]")
        legend = subplot.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), labels=cols_memory)
        legend.get_frame().set_facecolor('none')
        
        subplot = self.figure.add_subplot(1, 2, 2)
        subplot.set_facecolor('none')
        cols_swap = ['Used Swap', 'Free Swap']
        data_swap = data[cols_swap]
        subplot.pie(data_swap, autopct= lambda val: np.round(val/100 * np.sum(data_swap), 2),
                         colors=[colors['green'], colors['blue']],)
        legend = subplot.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), labels=cols_swap)
        legend.get_frame().set_facecolor('none')
        subplot.set_title("Swap Usage [GB]")
        self._draw_figure()


    def historical_plot(self):
        historical = self.dataSource.get_historical()
        if(len(historical)<4):
            return
        
        total_memory = self.dataSource.get_total_memory()
        time = historical.index.to_numpy()[-18:]
        used_memory = historical['Used Memory'].to_numpy()[-18:]
        used_swap = historical['Used Swap'].to_numpy()[-18:]
        time_smooth, used_memory_smooth = self._smooth_curve(time, used_memory, a_max=total_memory)
        time_smooth, used_swap_smooth = self._smooth_curve(time, used_swap, a_max=total_memory)

        self._clean_figure()
        subplot = self.figure.add_subplot()
        subplot.set_facecolor('none')
        subplot.plot(time_smooth, used_memory_smooth, markersize=12, label='Mem', color=colors['orange'])
        subplot.plot(time_smooth, used_swap_smooth, markersize=12, label='Swap', color=colors['green'])
        subplot.set_ylim(0, total_memory)
        subplot.set_ylabel('Used Memory [GB]')
        subplot.set_xlabel('Time [s]')
        subplot.set_title("Memory")
        legend = subplot.legend(loc='center right', bbox_to_anchor=(1.25, 0.5))
        legend.get_frame().set_facecolor('none')
        self._draw_figure()

