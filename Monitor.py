
import tkinter as tk
from threading import Thread
from tkinter import *

from Plotter import Plotter
from PlotterCPU import PlotterCPU
from PlotterNetwork import PlotterNetwork
from PlotterRAM import PlotterRAM
from PlotterStorage import PlotterStorage
from ProcessesUpdater import ProcessesUpdater
from Runnable import Runnable


class MonitorGUI:

    root:Tk
    runnables:list[Runnable] = []
    threads:list[Thread]

    def __init__(self):
        self.runnables = []
        self.threads = []
        self.root = Tk()
        self.build_root()
        self.launch_threads()
        self.root.mainloop()


    def build_root(self):
        self.root.title(f"Resource Monitor")
        self.root.resizable = False
        rootFrame = Frame(self.root)
        rootFrame.configure(border=3, relief=tk.GROOVE)
        rootFrame.grid()

        # RAM

        ramFrame = Frame(rootFrame)
        ramFrame.grid(row=0, column=0, padx=15, pady=10)
        ramPlotter = PlotterRAM(ramFrame)
        ramSaveBtn = Button(ramFrame, text="Save Historical",
                            command=ramPlotter.dataSource.save_file)
        ramSaveBtn.pack(side=BOTTOM, fill=BOTH)
        ramViewBtn = Button(ramFrame, text="Historical View",
                            command=lambda: self.toggle_plot(ramPlotter, ramViewBtn))
        ramViewBtn.pack(side=BOTTOM, fill=BOTH)
        self.runnables.append(ramPlotter)

        # Storage

        storageFrame = Frame(rootFrame)
        storageFrame.grid(row=1, column=0, padx=15, pady=10)
        storagePlotter = PlotterStorage(storageFrame)
        storageSaveBtn = Button(storageFrame, text="Save Snapshot",
                            command=storagePlotter.dataSource.save_file)
        storageSaveBtn.pack(side=BOTTOM, fill=BOTH)
        self.runnables.append(storagePlotter)

        # CPU

        cpuFrame = Frame(rootFrame)
        cpuFrame.grid(row=0, column=1, padx=15, pady=10)
        cpuPlotter = PlotterCPU(cpuFrame)
        cpuSaveBtn = Button(cpuFrame, text="Save Historical", 
                            command=cpuPlotter.dataSource.save_file)
        cpuSaveBtn.pack(side=BOTTOM, fill=BOTH)
        cpuViewBtn = Button(cpuFrame, text="Historical View",
                            command=lambda: self.toggle_plot(cpuPlotter, cpuViewBtn))
        cpuViewBtn.pack(side=BOTTOM, fill=BOTH)
        self.runnables.append(cpuPlotter)

        # Network

        networkFrame = Frame(rootFrame)
        networkFrame.grid(row=0, column=2, padx=15, pady=10)
        networkPlotter = PlotterNetwork(networkFrame)
        networkSaveBtn = Button(networkFrame, text="Save Historical", 
                            command=networkPlotter.dataSource.save_file)
        networkSaveBtn.pack(side=BOTTOM, fill=BOTH)
        networkViewBtn = Button(networkFrame, text="Historical View", command=
                                  lambda: self.toggle_plot(networkPlotter, networkViewBtn))
        networkViewBtn.pack(side=BOTTOM, fill=BOTH)
        self.runnables.append(networkPlotter)

        # Processes

        processesFrame = Frame(rootFrame)
        processesFrame.grid(row=1, column=1, columnspan=2, padx=15, pady=10)
        processesLabel = Label(processesFrame, text="Process List", font=('Arial',14,'bold'), pady=5)
        processesLabel.pack(side=TOP, fill=BOTH)
        processesTable = Frame(processesFrame, borderwidth=2, pady=15)
        processesTable.pack(side=BOTTOM, fill=BOTH)
        processesUpdater = ProcessesUpdater(processesTable)
        processesSaveBtn = Button(processesFrame, text="Save Snapshot",
                            command=processesUpdater.dataSource.save_file)
        processesSaveBtn.pack(side=BOTTOM, before=processesTable, fill=BOTH)
        self.runnables.append(processesUpdater)
        
        # Handle Exit

        self.root.protocol("WM_DELETE_WINDOW", self.on_click_exit)

    def launch_threads(self):
        for runnable in self.runnables:
            thread = Thread(target=runnable.run)
            self.threads.append(thread)
        for thread in self.threads:
            thread.start()

    def on_click_exit(self):
        for runnable in self.runnables:
            runnable.is_running = False
        for thread in self.threads:
            thread.join()
        print("Monitor Finished")
        self.root.destroy()

    def toggle_plot(self, plotter:Plotter, btn:Button):
        plotter.toggle_plot()
        if plotter.is_historical_active:
            btn.config(text='Standard View')
        else:
            btn.config(text='Historical View')


if __name__ == '__main__':
    gui = MonitorGUI()
    
