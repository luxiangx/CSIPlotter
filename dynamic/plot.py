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
from dynamic import load_csi_data
from dynamic.init import RealtimePlotter


class Plotter(RealtimePlotter):

    def __init__(self):

        RealtimePlotter.__init__(self, [(-1, +1), (-1, +1)],
                                 # phaselims=((-1,+1), (-1,+1)),
                                 window_name='CSIwave demo',
                                 yticks=[(0, 35, +70), (-3.14, 0, +3.14)],
                                 styles=['r-', 'b-'],
                                 ylabels=['Amplitude', 'phase'])

        self.xcurr = 0

    def getValues(self):
        start = time.clock()
        s, c = self.get_amti_and_angle()
        end = time.clock()
        print('time：', end - start)
        return s, c

    def get_amti_and_angle(self):
        from time import sleep
        global offset
        global amti
        global angle
        csi_trace, offset = file_data, offset = load_csi_data.read_bf_file(filepath, offset)
        len = np.size(csi_trace)

        print('len：', len)
        if (len >= 1):

            csi_entry = csi_trace[len - 1]
            csi = load_csi_data.get_scale_csi(csi_entry)
            # print(csi)
            a, j, k = np.shape(csi)
            if a == 1 and j == 3 and k == 30:
                csi = csi[0][:][:]
                csi_1 = csi[:][0][:]
                csi_1 = csi_1.squeeze()

                amti = abs(csi_1.T)[1]
                angle = getTruePhase(csi_1.T)
        # sleep(.0001)

        return amti, angle


# def _update(plotter):
#
#     from time import sleep
#
#     while True:
#
#         plotter.xcurr += 1
#         sleep(.001)


def getTruePhase(subcarriers):
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


def plot():
    # import threading
    offset = 0
    amti = 0
    angle = 0
    filepath = '/home/luxiang/linux-80211n-csitool-supplementary/data/1.dat'
    file_data, offset = load_csi_data.read_bf_file(filepath, offset)
    plotter = Plotter()

    # thread = threading.Thread(target = _update, args = (plotter,))
    # thread.daemon = True
    # thread.start()

    plotter.start()
