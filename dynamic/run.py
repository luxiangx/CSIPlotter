from time import sleep

from dynamic import load_csi_real_time_data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')


def run(widget_Canvas, flag, mode, antenna_tx, antenna_rx, subcarrier_no, filepath):

    # def read_data(offset):
    #     file_data, offset = load_csi_real_time_data.read_bf_file(filepath, offset)
    #     if len(file_data) > 0:
    #         csi_entry = file_data.loc[0]
    #         csi = load_csi_real_time_data.get_scale_csi(csi_entry)
    #         return abs(np.squeeze(csi)), offset
    #     else:
    #         return None

    def update(value):
        widget_Canvas.tx = ord(antenna_tx) - ord('A')
        widget_Canvas.rx = ord(antenna_rx) - ord('A')
        widget_Canvas.subcarriers = int(subcarrier_no)


    def get_single_subcarrier_value(offset):
        while flag:
            res = read_data(offset)
            if not res:
                sleep(0.05)
                print(1)
            else:
                csi_matrix, offset = res[0], res[1]
                update(csi_matrix[ord(antenna_rx) - ord('A'), int(subcarrier_no)])


    def get_antenna_pair_value(offset):
        while flag:
            csi_matrix[0, :, :, :], offset = read_data(offset)
            update(csi_matrix[0, ord(antenna_tx) - ord('A'), ord(antenna_rx) - ord('A'), :])

    def get_all_data_value(offset):
        while flag:
            csi_matrix[0, :, :, :], offset = read_data(offset)
            update(csi_matrix[0, :, :, :])

    widget_Canvas.start()
    file_data, offset = load_csi_real_time_data.read_bf_file(filepath, 0)
    n_tx = file_data.loc[0, 'Ntx']
    if ord(antenna_tx) - ord('A') >= n_tx:
        return

    csi_matrix = np.empty([1, n_tx, 3, 30], dtype=float)

    if mode == '子载波显示':
        get_single_subcarrier_value(offset)
    elif mode == '天线对显示':
        get_antenna_pair_value(offset)
    elif mode == '全数据显示':
        get_all_data_value(offset)
    else:
        pass
