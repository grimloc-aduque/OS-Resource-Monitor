
import tkinter as tk

from matplotlib.figure import Figure

from DataSourceCPU import DataSourceCPU
from Plotter import Plotter


class PlotterCPU(Plotter):

    def __init__(self, frame:tk.Frame):
        super().__init__(frame)
        self.dataSource = DataSourceCPU()
        
    def generate_figure(self):
        return Figure(figsize=(6, 4), dpi=80)

    def plot(self):
        self._clean_figure()
        data = self.dataSource.get_data()
        subplot = self.figure.add_subplot()
        subplot.set_facecolor('none')
        subplot.bar(data.index, [100]*len(data))
        subplot.bar(data.index, data)
        subplot.set_title("CPU Usage")
        subplot.set_xlabel("CPUs")
        subplot.set_ylabel("% Usage")
        self._draw_figure()

    def historical_plot(self):
        historical = self.dataSource.get_historical()
        if(len(historical)<4):
            return
        self._clean_figure()
        subplot = self.figure.add_subplot()
        subplot.set_facecolor('none')
        for col in historical.columns:
            time = historical.index[-18:]
            usage = historical[col].to_numpy()[-18:]
            time_smooth, usage_smooth = self._smooth_curve(time, usage, a_max=100)
            subplot.plot(time_smooth, usage_smooth, label=col)
        
        subplot.set_ylim(0, 100)
        subplot.set_title("CPU Usage")
        subplot.set_ylabel('% Usage')
        subplot.set_xlabel('Time [s]')
        legend = subplot.legend(loc='center right', bbox_to_anchor=(1.25, 0.5))
        legend.get_frame().set_facecolor('none')
        self._draw_figure()

