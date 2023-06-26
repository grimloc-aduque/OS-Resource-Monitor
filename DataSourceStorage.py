
import pandas as pd
import psutil

from DataSource import DataSource


class DataSourceStorage(DataSource):

    data:pd.DataFrame

    def update_data(self):
        data = []
        partitions = self._get_partitions()
        for partition in partitions:
            device = partition[0]
            path = partition[1]
            try:
                data.append(pd.Series(
                    {
                        "Device": device,
                        "Path": path,
                        "Total Size": self._get_total_size(path),
                        "Free Size": self._get_free_size(path),
                        "Used Size": self._get_used_size(path),
                        "Percentage": self._get_percent(path)
                    }))
            except FileNotFoundError:
                continue
        self.data = pd.DataFrame(data)

    def get_data(self):
        return self.data

    def get_historical(self):
        raise Exception("Historical Unavailable")
    
    def save_file(self):
        self.data.to_csv(f'{self.output_folder}/storage_snapshot.csv', index=False)

    # System Information

    def _get_partitions(self,):
        return psutil.disk_partitions()

    def _get_total_size(self, path):
        return self.to_GB(psutil.disk_usage(path)[0])
    
    def _get_used_size(self, path):
        return self.to_GB(psutil.disk_usage(path)[1])
    
    def _get_free_size(self, path):
        return self.to_GB(psutil.disk_usage(path)[2])
    
    def _get_percent(self, path):
        return psutil.disk_usage(path)[3]