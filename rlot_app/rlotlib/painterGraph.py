import os
import matplotlib.pyplot as plt
from datetime import datetime
from . import (
    generateFio,
    checks
)


def get_output_dir_for_graph():
    root_proj_path = os.path.dirname(os.path.dirname(os.path
                                                     .dirname(os.path.abspath(__file__))))
    path = os.path.join(root_proj_path, "graphs")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_current_data():
    return datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

# with open(path_to_logs, 'r') as logFile:
#     data = [[int(j.rstrip()) for j in i.split(',')]
#             for i in logFile.readlines()]


def get_all_logs_files(path_to_logs):
    data_logs = []
    for file_name in os.listdir(path_to_logs):
        if file_name.endswith(".log"):
            data_logs.append(file_name)

    return data_logs


def filter_data_logs(settings, data_logs_array):

    mode = checks.define_mode_dev(settings)
    log_dict = {}
    for rw in [i.strip() for i in settings["global"]["rw"].split(',')]:

        log_dict[rw] = {}
        for type_graph in ["iops", "lat", "bw", "slat", "clat"]:
            log_dict[rw][type_graph] = []

        for logs in data_logs_array:
            for type_graph in ["iops", "lat", "bw", "slat", "clat"]:
                if logs.startswith(f"{settings['global']['bs']}-{rw}-{mode}.results_{type_graph}"):
                    log_dict[rw][type_graph].append(logs)
    return log_dict


def draw_graph(title, rw, logs_array, path_to_graph_dir, dir_for_logs, type_graph):
    X, Y = [], []
    for log_file in logs_array:
        f = open(f"{dir_for_logs}/{log_file}", "r")
        data = [[int(j.rstrip()) for j in i.split(',')] for i in f.readlines()]
        for index, rows in enumerate(data):
            if len(X) < index + 1:
                X.append((rows[0] + 1) // 1000)
                Y.append(rows[1])
            else:
                X[index] += (rows[0] + 1) // 1000
                Y[index] += rows[1]
        f.close()
    X = [X[i] // len(logs_array) for i in range(len(X))]
    Y = [Y[i] // len(logs_array) for i in range(len(Y))]

    # print()
    # print(Y, title)
    # print()
    plt.plot(X, Y)
    plt.title(title)
    plt.xlabel("Time(s)")
    plt.ylabel(type_graph)
    plt.margins(0)
    plt.savefig(f"{path_to_graph_dir}/{title}-{get_current_data()}.png")


def draw(path_to_logs, path_to_graph_dir, settings):
    data_logs = get_all_logs_files(path_to_logs)
    dict = filter_data_logs(settings, data_logs)

    for rw in dict:
        for type_graph in dict[rw]:
            draw_graph(f"{rw}_graph_{type_graph}", rw,
                       dict[rw][type_graph], path_to_graph_dir, path_to_logs, type_graph)
