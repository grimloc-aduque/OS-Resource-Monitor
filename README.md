# OS-Resource-Monitor

# Technologies
Python
* GUI (tkinter)
* Plotting (matplotlib, pandas)
* Parallelization (threading)
* System information (psutil)


# Monitor
Python implementation of a real-time monitor for compute resources
* RAM
* CPU
* Network
* Storage
* Processes

## Standard View

<img src="./Images/monitor_standard_view.png" style="width:400px;"/>

## Historical View

<img src="./Images/monitor_historical_view.png" style="width:400px;"/>


# Class Diagram

MVC implementation
* Model (DataSources)
* View (Monitor)
* Controller (Runnables: Plotters/ProcessesUpdater)

<img src="./Images/class_diagram.png" style="width:400px;"/>