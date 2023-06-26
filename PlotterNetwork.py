
import tkinter as tk

import numpy as np
from matplotlib.figure import Figure

from colors import colors
from DataSourceNetwork import DataSourceNetwork
from Plotter import Plotter


class PlotterNetwork(Plotter):

    def __init__(self, frame:tk.Frame):
        super().__init__(frame)
        self.dataSource = DataSourceNetwork()

    def generate_figure(self):
        return Figure(figsize=(5, 4), dpi=80)

    def plot(self):
        self._clean_figure()
        data = self.dataSource.get_data()
        subplot = self.figure.add_subplot()
        subplot.set_facecolor('none')
        subplot.bar(data.index, data, color=[colors['red'], colors['blue']])
        subplot.set_ylim(bottom=0)
        subplot.set_title("Network")
        subplot.set_ylabel('Speed [KB/s]')
        self._draw_figure()


    def historical_plot(self):
        historical = self.dataSource.get_historical()
        if(len(historical)<5):
            return
        
        time = historical.index[1:][-18:]
        bytes_up = np.diff(historical['Bytes Sending'])[-18:]
        bytes_down = np.diff(historical['Bytes Receiving'])[-18:]
        time_smooth, bytes_up_smooth = self._smooth_curve(time, bytes_up)
        time_smooth, bytes_down_smooth = self._smooth_curve(time, bytes_down)

        self._clean_figure()
        subplot = self.figure.add_subplot()
        subplot.set_facecolor(colors['gray'])
        subplot.plot(time_smooth, bytes_up_smooth, label='↑ ', color=colors['blue'])
        subplot.plot(time_smooth, bytes_down_smooth, label='↓', color=colors['red'])
        subplot.set_ylim(bottom=0)
        subplot.set_title("Network")
        subplot.set_xlabel('Time [s]')
        subplot.set_ylabel('Speed [KB/s]')
        legend = subplot.legend(loc='center right', bbox_to_anchor=(1.25, 0.5))
        legend.get_frame().set_facecolor('none')
        self._draw_figure()


