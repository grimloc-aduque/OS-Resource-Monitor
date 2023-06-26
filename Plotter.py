
import tkinter as tk
from abc import abstractmethod

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.interpolate import make_interp_spline

from colors import colors
from DataSource import DataSource
from Runnable import Runnable


class Plotter(Runnable):

    dataSource:DataSource
    figure:Figure
    canvas:FigureCanvasTkAgg
    is_historical_active:bool

    def __init__(self, frame:tk.Frame):
        super().__init__()
        self.figure = self.generate_figure()
        self.figure.set_facecolor(colors['gray'])
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
        self.is_historical_active = False


    def run_actions(self):
        self.dataSource.update_data()
        if self.is_historical_active:
            self.historical_plot()
        else:
            self.plot()

    @abstractmethod
    def generate_figure(self):
        pass

    @abstractmethod
    def plot(self):
        pass

    @abstractmethod
    def historical_plot(self):
        pass

    def _clean_figure(self):
        self.figure.clf()

    def _draw_figure(self):
        self.figure.tight_layout()
        self.canvas.draw()

    def _smooth_curve(self, x, y, a_min=0, a_max=None):
        x_smooth = np.linspace(x.min(),x.max(),300)
        y_smooth = make_interp_spline(x, y)(x_smooth)
        y_smooth = y_smooth.clip(a_min, a_max)
        return x_smooth, y_smooth
    
    def toggle_plot(self):
        self.is_historical_active = not self.is_historical_active
