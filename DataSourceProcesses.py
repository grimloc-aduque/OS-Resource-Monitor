
import numpy as np
import pandas as pd
import psutil

from DataSource import DataSource


class DataSourceProcesses(DataSource):

    data:pd.DataFrame

    def update_data(self):
        data = []
        pids_list=psutil.pids()
        for pid in pids_list:
            try: 
                process = self._get_process(pid)
            except psutil.NoSuchProcess:
                continue
            data.append({
                "PID": pid,
                "Name": process.name(),
                "User": process.username(),
                "CPU Time": self._get_cpu(process),
                "Memory [GB]": self._get_memory(process),
                "Status": process.status()
            })
        self.data = pd.DataFrame(data)

    def get_data(self):
        return self.data

    def get_historical(self):
        raise Exception("Historical Unavailable")

    def save_file(self):
        self.data.to_csv(f'{self.output_folder}/processes_snapshot.csv', index=False)

    # System information

    def _get_process(self, pid):
        return psutil.Process(pid)
    
    def _get_cpu(self, process):
        return process.cpu_times()[0]

    def _get_memory(self, process):
        return np.round(process.memory_info()[0]/(10**9), 2)



