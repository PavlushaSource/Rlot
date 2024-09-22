import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
from datetime import datetime
from lib.utils import get_root_path, define_mode_dev



class Painter:
    def __init__(self, path_to_logs, settings):
        self.path_to_logs = path_to_logs
        self.path_to_out = self.__create_output_dir()
        self.settings = settings

    def __create_output_dir(self) -> str:
        root_path = get_root_path()
        path = root_path + "/out/graphs"
        os.makedirs(path, exist_ok=True)
        return path


    def __get_all_logs_files(self) -> list[str]:
        data_logs = []
        for file_name in os.listdir(self.path_to_logs):
            if file_name.endswith(".log"):
                data_logs.append(file_name)

        return data_logs
    
    def __get_data_logs_dict(self) -> dict:
        logs_dict = {}
        all_logs = self.__get_all_logs_files()
        mode = define_mode_dev(self.settings)

        for rw in [i.strip() for i in self.settings["global"]["rw"].split(",")]:

            logs_dict[rw] = {}
            for type_graph in ["iops", "lat", "bw", "slat", "clat"]:
                logs_dict[rw][type_graph] = []

            for logs in all_logs:
                for type_graph in ["iops", "lat", "bw", "slat", "clat"]:
                    if logs.startswith(
                        f"{self.settings['global']['bs']}-{rw}-{mode}.results_{type_graph}"
                    ):
                        logs_dict[rw][type_graph].append(logs)
        return logs_dict
    

    def __calculate_one_job(self, data_path) -> list[int]:
        with open(data_path, 'r') as log_file:
            data = [[int(j.rstrip()) for j in i.split(",")] for i in log_file.readlines()]

            size_array = int(self.settings['global']['runtime'])
            result_array = [0] * size_array


            # row format here - https://fio.readthedocs.io/en/latest/fio_doc.html#log-file-formats
            for row in data:
                if row[0] // 1000 >= size_array:
                    break
                result_array[row[0] // 1000] += row[1]
            
            return result_array

    def __calculate_avg_all_jobs(self, logs_path_array):

        result_array = np.array()
        for log_path in logs_path_array:
            one_jobs_result_array = self.__calculate_one_job(log_path)
            result_array = np.vstack((result_array, one_jobs_result_array))

        avg_result_array = np.mean(result_array, axis=0)
        return avg_result_array


    def __draw_graph(self, Y_array, confidence_interval: tuple, title: str, y_label: str):
        X_array = list(range(1, len(Y_array) + 1))
        plt.plot(X_array, Y_array)
        plt.title(title)
        plt.ylabel(y_label)
        plt.xlabel(f"time in (seconds)) / confidence interval 95%=({confidence_interval[0]};{confidence_interval[1]})")
        plt.savefig(f"{self.path_to_out}/{title}.png")


    def draw_graph(self):
        logs_dict = self.__get_data_logs_dict()

        for rw in logs_dict:
            for type_graph in logs_dict[rw]:
                logs_path_array = logs_dict[rw][type_graph]

                avg_data_array = self.__calculate_avg_all_jobs(logs_path_array)

                confidence_interval = st.t.interval(0.95, len(avg_data_array) - 1, loc=np.mean(avg_data_array), scale=st.sem(avg_data_array))


                self.__draw_graph(avg_data_array, confidence_interval, f"{rw}_{type_graph}_graph", type_graph)
