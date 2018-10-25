#!/usr/bin/env python
'''
Real-time plot demo using sine waves.

Copyright (C) 2015 Simon D. Levy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
'''

import numpy as np
import time

# Simple example with threading
from dynamic import load_csi_real_time_data
from dynamic.RealtimePlotter import RealtimePlotter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

filepath = '/home/luxiang/1.dat'
offset = 0
amti = 0
angle = 0


class Plotter(RealtimePlotter):

    def __init__(self):
        RealtimePlotter.__init__(self,
                                 yticks=(0, 35, +70),
                                 styles='r-',
                                 ylabels='Amplitude')

        # self.xcurr = 0
        self.tx = 'A'
        self.rx = 'A'
        self.subcarrier_no = '1'
        self.mode = '子载波显示'
        self.data = '幅值'
        self.offset = 0
        self.last_value = None


    def getValues(self):
        start = time.clock()
        r = self.get_values_by_mode()
        end = time.clock()
        # print('time：', end - start)
        # print(r)
        return r

    def get_single_subcarrier_amplitude_value(self):
        file_data, self.offset = load_csi_real_time_data.read_bf_file(filepath, self.offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[len(file_data) - 1]
            csi = load_csi_real_time_data.get_scale_csi(csi_entry)
            return abs(np.squeeze(csi[ord(self.tx) - ord('A')][ord(self.rx) - ord('A')][int(self.subcarrier_no)]))
        else:
            return self.last_value

    def get_antenna_pair_amplitude_value(self):
        pass

    def get_all_data_amplitude_value(self):
        pass

    def get_single_subcarrier_phase_value(self):
        pass

    def get_antenna_pair_phase_value(self):
        pass

    def get_all_data_phase_value(self):
        pass

    def get_values_by_mode(self):
        # from time import sleep
        # global offset
        # global amti
        # global angle
        # # global filepath
        # file_data, offset = load_csi_real_time_data.read_bf_file(
        #     '/home/luxiang/linux-80211n-csitool-supplementary/data/1.dat', offset)
        # len = np.size(file_data)
        #
        # print('len：', len)
        # if len >= 1:
        #     csi_entry = file_data.loc[0]
        #     csi = load_csi_real_time_data.get_scale_csi(csi_entry)
        #     # print(csi)
        #     # a, j, k = np.shape(csi)
        #     csi_1 = csi[0][0][:]
        #     amti = abs(np.squeeze(csi[0][0][23]))
        #     angle = get_true_phase(csi_1.T)
        # sleep(.01)
        # return amti

        if self.data == '幅值':
            if self.mode == '子载波显示':
                self.last_value = self.get_single_subcarrier_amplitude_value()
                return self.last_value
            elif self.mode == '天线对显示':
                return self.get_antenna_pair_amplitude_value()
            elif self.mode == '全数据显示':
                return self.get_all_data_amplitude_value()
            else:
                pass
        elif self.data == '相位':
            if self.mode == '子载波显示':
                return self.get_single_subcarrier_phase_value()
            elif self.mode == '天线对显示':
                return self.get_antenna_pair_phase_value()
            elif self.mode == '全数据显示':
                return self.get_all_data_phase_value()
            else:
                pass


# def _update(plotter):
#     from time import sleep
#
#     while True:
#         plotter.xcurr += 1
#         sleep(.001)


def get_true_phase(subcarriers):
    import math
    subcarriers = np.angle(subcarriers)
    Temp = np.zeros(30)
    recycle = 0
    Temp[0] = subcarriers[0]
    for t_i in range(1, 30):
        if subcarriers[t_i] - subcarriers[t_i - 1] > math.pi:
            recycle = recycle + 1
        Temp[t_i] = subcarriers[t_i] - recycle * 2 * math.pi

    subcarriers = Temp.T
    k_index_i = np.array([-28, -26, -24, -22, -20, -18, -16, -14, -12, -10, -8, -6, -4, -2, -1,
                          1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 28]).T
    # k_index_i = np.array([-58, -54, -50, -46, -42, -38, -34, -30, -26, -22, -18, -14, -10, -6, -2,
    #                       2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58]).T
    a = (subcarriers[29] - subcarriers[0]) / 56
    b = np.mean(subcarriers)
    new_one_road_subcarrier_30_angle = subcarriers - a * k_index_i - b

    return new_one_road_subcarrier_30_angle[23]

# def plot():
#     global offset
#     _, offset = load_csi_real_time_data.read_bf_file(filepath, offset)
#     plotter = Plotter()
#     plotter.start()
