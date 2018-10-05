from time import sleep

from static import load_csi_data
import numpy as np
import matplotlib.pyplot as plt


def run(flag, mode, antenna_tx, antenna_rx, subcarrier_no, filepath):
    def read_data(offset):
        file_data, offset = load_csi_data.read_bf_file(filepath, offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[-1]
            csi = load_csi_data.get_scale_csi(csi_entry)
            return abs(np.squeeze(csi)), offset

    def update(value):
        pass

    def get_single_subcarrier_value(offset):
        while flag:
            csi_matrix[0, :, :, :], offset = read_data(offset)
            update(csi_matrix[0, ord(antenna_tx) - ord('A'), ord(antenna_rx) - ord('A'), subcarrier_no])

    def get_antenna_pair_value(offset):
        while flag:
            csi_matrix[0, :, :, :], offset = read_data(offset)
            update(csi_matrix[0, ord(antenna_tx) - ord('A'), ord(antenna_rx) - ord('A'), :])

    def get_all_data_value(offset):
        while flag:
            csi_matrix[0, :, :, :], offset = read_data(offset)
            update(csi_matrix[0, :, :, :])

    file_data, offset = load_csi_data.read_bf_file(filepath, 0)
    n_tx = file_data.loc[0, 'Ntx']
    if ord(antenna_tx) - ord('A') >= n_tx:
        return

    csi_matrix = np.empty([1, n_tx, 3, 30], dtype=float)

    if mode == '单子载波显示':
        get_single_subcarrier_value()
    elif mode == '天线对显示':
        get_antenna_pair_value()
    elif mode == '全数据显示':
        get_all_data_value()
    else:
        pass
