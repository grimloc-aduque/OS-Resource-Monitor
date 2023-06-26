
import tkinter as tk

from matplotlib.figure import Figure

from colors import colors
from DataSourceStorage import DataSourceStorage
from Plotter import Plotter


class PlotterStorage(Plotter):

    def __init__(self, frame:tk.Frame):
        super().__init__(frame)
        self.dataSource = DataSourceStorage()

    def generate_figure(self):
        return Figure(figsize=(6, 6), dpi=80)

    def plot(self):
        self._clean_figure()
        data = self.dataSource.get_data()
        subplot = self.figure.add_subplot()
        subplot.set_facecolor('none')
        devices = data['Path']
        percentage = data['Percentage']
        subplot.barh(devices, [100]*len(devices), color=colors['green'])
        subplot.barh(devices, percentage, color=colors['blue'])
        subplot.set_title("Storage")
        for i in range (len(data)):
            bar = subplot.patches[i]
            used_size = data.loc[i]['Used Size']
            total_size = data.loc[i]['Total Size']
            text = f'  {used_size}GB / {total_size}GB'
            subplot.text(0.1, bar.get_y()+bar.get_height()/2, text, color = 'black', ha = 'left', va = 'center', )

        self._draw_figure()


    def historical_plot(self):
        raise Exception("Historical Unavailable")
