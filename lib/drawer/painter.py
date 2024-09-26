import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
from lib.utils import get_root_path, define_mode_dev, get_current_data, get_current_data_short



class Painter:
    def __init__(self, path_to_logs, settings, mode, dev_name):
        self.path_to_logs = path_to_logs
        self.path_to_out = self.__create_output_dir()
        self.settings = settings
        self.mode_bdev = mode
        self.dev_name = dev_name

    def __create_output_dir(self) -> str:
        root_path = get_root_path()
        path = root_path + "/out/graphs" + f"/{get_current_data()}"
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

        for rw in [i.strip() for i in self.settings["global"]["rw"].split(",")]:

            logs_dict[rw] = {}
            for type_graph in ["iops", "lat", "bw", "slat", "clat"]:
                logs_dict[rw][type_graph] = []

            for logs in all_logs:
                for type_graph in ["iops", "lat", "bw", "slat", "clat"]:
                    if logs.startswith(
                        f"{self.settings['global']['bs']}-{rw}-{self.mode_bdev}.results_{type_graph}"
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

        result_array = None
        for log_path in logs_path_array:
            log_relative_path = f"{self.path_to_logs}/{log_path}"
            one_jobs_result_array = self.__calculate_one_job(log_relative_path)

            if not isinstance(result_array, np.ndarray):
                result_array = np.array(one_jobs_result_array)
            else:
                result_array = np.vstack((result_array, one_jobs_result_array))


        all_result_array = result_array
        if len(result_array.shape) != 1:
            all_result_array = np.sum(result_array, axis=0)
        
        # print(f"ALL JOBS RESULT ARRAY", all_result_array)
        # print("\n\n")
        
        return all_result_array


    def __draw_graph(self, Y_array, confidence_interval: tuple, title: str, y_label: str, right_title = None, left_title = None, rw = "", type_graph = ""):
        X_array = list(range(1, len(Y_array) + 1))

        iodepth = self.settings['global']['iodepth']
        numjobs = self.settings['global']['numjobs']

        avg_data = np.mean(Y_array, axis=0)
        l_bord_CI, r_bord_CI = round(confidence_interval[0]), round(confidence_interval[1])

        fig, ax1 = plt.subplots()

        ax1.plot(X_array, Y_array)
        
        ax1.ticklabel_format(useOffset=False, style='plain')

        ticks = ax1.get_yticks()
        size_delim_y = ticks[1] - ticks[0]
        # ax1.text(0.15, size_delim_y * 0.2, f"Confidence interval 95%: ({round(confidence_interval[0])};{round(confidence_interval[1])})")
        # ax1.text(0.15, size_delim_y * 0.4, f"Avg: {np.mean(Y_array, axis=0)}")

        ax1.set_title(f"avg={round(avg_data)} | CI 95%=({l_bord_CI}, {r_bord_CI})", fontsize=16)
        ax1.set_title(right_title, loc='right', fontsize=12)
        ax1.set_title(left_title, loc='left', fontsize=12)
        ax1.set_ylim(0, None)
        ax1.set_ylabel(y_label, fontsize=12)
        ax1.set_xlabel(f"time in (seconds)", fontsize=12)

        fig.set_size_inches(15, 8)
        fig.suptitle(title, fontsize=20)
        fig.savefig(f"{self.path_to_out}/{rw}_{type_graph}_i{iodepth}_n{numjobs}_graph.png", dpi=100)


    def draw_graph(self):
        logs_dict = self.__get_data_logs_dict()

        for rw in logs_dict:
            for type_graph in logs_dict[rw]:
                logs_path_array = logs_dict[rw][type_graph]

                avg_data_array = self.__calculate_avg_all_jobs(logs_path_array)

                if type_graph == "bw":
                    convert_to_MiB = lambda x: round(x / (1024))
                    avg_data_array = np.array([convert_to_MiB(t) for t in avg_data_array])

                if type_graph in ["clat", "lat", "slat"]:
                    convert_to_ms = lambda x: round(x / 1e6)
                    avg_data_array = np.array([convert_to_ms(t) for t in avg_data_array])

                confidence_interval = st.t.interval(0.95, len(avg_data_array) - 1, loc=np.mean(avg_data_array), scale=st.sem(avg_data_array))

                print(f"RW - {rw}, TYPE DATA - {type_graph}, ARRAY - {avg_data_array}")
                print("\n")

                center_title = f"Graph for {self.dev_name}"
                left_title = get_current_data_short()
                right_title = f"| rw {rw} | iodepth {self.settings['global']['iodepth']} | numjobs {self.settings['global']['numjobs']}"

                self.__draw_graph(avg_data_array, confidence_interval, center_title, type_graph, right_title, left_title, rw, type_graph)
