# -*- coding: utf-8 -*-
"""
Real-time scrolling multi-plot over time.

Requires: matplotlib
          numpy

Adapted from example in http://stackoverflow.com/questions/8955869/why-is-plotting-with-matplotlib-so-slow

Copyright (C) 2015 Simon D. Levy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
"""
import os
import subprocess
import threading
import matplotlib
import matplotlib.animation as animation
import numpy as np
from matplotlib.figure import Figure
from dynamic import load_csi_real_time_data

matplotlib.use('Qt5Agg')


class RealtimePlotter(object):
    """
    Real-time scrolling multi-plot over time.  Your data-acquisition code should run on its own thread,
    to prevent blocking / slowdown.
    """
    ani = None
    error_no = 0
    """
    1: 发射天线选择错误，没有天线B
    2: 发射天线选择错误，没有天线C
    3: 
    """

    def __init__(self, ui):
        self.ui = ui
        self.size = 200
        self.styles = 'r-'
        self.xlabels = "Time"
        self.ylabels = "Amplitude"
        self.yticks = (0, 35, 70)
        self.legend = None
        self.interval_msec = 100000
        self.tx = 'A'
        self.rx = 'A'
        self.subcarrier_no = '1'
        self.mode = 'subcarrier'
        self.data = 'amplitude'
        self.offset = 0
        self.last_value = None
        self.filename = ""
        self.fig = Figure(figsize=(10, 20), dpi=100, tight_layout=True)
        # X values are arbitrary ascending; Y is initially zero
        self.x = np.arange(0, self.size)
        y = np.zeros(self.size)
        self.pause_flag = False
        self.start_flag = False
        self.last_line = None

        self.axes = self.fig.add_subplot(111)

        # Create lines
        self.lines = []
        style = self.styles
        ax = self.axes

        styles_for_row = style if type(style) == tuple else [style]
        for k in range(len(styles_for_row)):
            self.lines.append(ax.plot(self.x, y, styles_for_row[k], animated=True)[0])
        if self.legend is not None and len(self.legend) > 0:
            ax.legend()

        # Add properties as specified
        ax.set_xlabel(self.xlabels, fontsize=15)
        ax.set_ylabel(self.ylabels, fontsize=15)

        # Set axis limits
        ax.set_xlim(0, self.size)

        # Set ticks and gridlines
        ax.yaxis.set_ticks(self.yticks)
        ax.yaxis.grid(True)
        ax.yaxis.set_visible(True)

        # XXX Hide X axis ticks and labels for now
        # ax.xaxis.set_visible(False)
        # Allow interval specification

    def start(self):
        t = threading.Thread(target=self.log())
        t.start()
        RealtimePlotter.ani = animation.FuncAnimation(self.fig, self.animate, blit=True,
                                                      interval=self.interval_msec)

    def get_values(self):
        r = self.get_values_by_mode()
        return r

    def get_values_by_mode(self):
        if self.data == 'amplitude':
            self.yticks = (-3.14, 0, +3.14)
            if self.mode == 'subcarrier':
                self.last_value = self.get_single_subcarrier_amplitude_value()
                if RealtimePlotter.error_no == 1:
                    self.stop_log()
                    self.fig.text(0.4, 0.6, 'DO NOT HAVE TX_B!', fontsize=25, color='R')
                elif RealtimePlotter.error_no == 2:
                    self.stop_log()
                    self.fig.text(0.4, 0.6, 'DO NOT HAVE TX_C!', fontsize=25, color='R')
                else:
                    return self.last_value
            elif self.mode == 'antenna pair':
                return self.get_antenna_pair_amplitude_value()
            elif self.mode == 'all data':
                return self.get_all_data_amplitude_value()
            else:
                pass

        elif self.data == 'phase':
            if self.mode == 'subcarrier':
                self.last_value = self.get_single_subcarrier_phase_value()
                if RealtimePlotter.error_no == 1:
                    self.stop_log()
                    self.fig.text(0.4, 0.7, 'DO NOT HAVE TX_B!', fontsize=25, color='R')
                elif RealtimePlotter.error_no == 2:
                    self.stop_log()
                    self.fig.text(0.4, 0.7, 'DO NOT HAVE TX_C!', fontsize=25, color='R')
                else:
                    return self.last_value
            elif self.mode == 'antenna pair':
                return self.get_antenna_pair_phase_value()
            elif self.mode == 'all data':
                return self.get_all_data_phase_value()
            else:
                pass
        self.reset_error_no()

    def animate(self, _):
        if self.pause_flag is True:
            return self.last_line
        values = self.get_values()
        yvals = values
        RealtimePlotter.rolly(self.lines[0], yvals)
        self.last_line = self.lines
        return self.lines

    def log(self):
        subprocess.call(
            "cd " + self.filename[:self.filename.find(self.filename.split("/")[-1])] +
            "; sudo /home/luxiang/linux-80211n-csitool-supplementary/netlink/log_to_file " +
            self.filename.split("/")[-1] + "&", shell=True)

    def stop_log(self):
        os.system("sudo kill -s 9 `ps -ef|grep '../netlink/log_to_file'|grep -v sudo|grep -v grep|awk '{print $2}'`")
        self.ui.add_msg('-> Stop showing!')
        self.pause_flag = True
        self.pause()
        self.start_flag = False

    def get_single_subcarrier_amplitude_value(self):
        file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[len(file_data) - 1]
            csi = load_csi_real_time_data.get_scale_csi(csi_entry)
            try:
                return abs(np.squeeze(csi[self.tx][self.rx][self.subcarrier_no]))
            except IndexError:
                RealtimePlotter.error_no = 1 if self.tx == 1 else 2
        else:
            return self.last_value

    def get_antenna_pair_amplitude_value(self):
        pass

    def get_all_data_amplitude_value(self):
        pass

    def get_single_subcarrier_phase_value(self):
        file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[len(file_data) - 1]
            csi = load_csi_real_time_data.get_scale_csi(csi_entry)
            try:
                return self.get_true_phase(csi[self.tx][self.rx][:], self.subcarrier_no)
            except IndexError:
                RealtimePlotter.error_no = 1 if self.tx == 1 else 2
                self.pause()
        else:
            return self.last_value

    def get_antenna_pair_phase_value(self):
        pass

    def get_all_data_phase_value(self):
        pass

    @classmethod
    def roll(cls, getter, setter, line, newval):
        data = getter(line)
        data = np.roll(data, -1)
        data[-1] = newval
        setter(data)

    @classmethod
    def rollx(cls, line, newval):
        RealtimePlotter.roll(line.get_xdata, line.set_xdata, line, newval)

    @classmethod
    def rolly(cls, line, newval):
        RealtimePlotter.roll(line.get_ydata, line.set_ydata, line, newval)

    @staticmethod
    def pause():
        RealtimePlotter.ani.event_source.stop()

    @staticmethod
    def reset_error_no():
        RealtimePlotter.error_no = 0

    @staticmethod
    def get_true_phase(subcarriers, index):
        import math
        subcarriers = np.angle(subcarriers)
        temp = np.zeros(30)
        recycle = 0
        temp[0] = subcarriers[0]
        for t_i in range(1, 30):
            if subcarriers[t_i] - subcarriers[t_i - 1] > math.pi:
                recycle = recycle + 1
            temp[t_i] = subcarriers[t_i] - recycle * 2 * math.pi

        subcarriers = temp.T
        k_index_i = np.array([-28, -26, -24, -22, -20, -18, -16, -14, -12, -10, -8, -6, -4, -2, -1,
                              1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 28]).T
        # k_index_i = np.array([-58, -54, -50, -46, -42, -38, -34, -30, -26, -22, -18, -14, -10, -6, -2,
        #                       2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58]).T
        a = (subcarriers[29] - subcarriers[0]) / 56
        b = np.mean(subcarriers)
        new_one_road_subcarrier_30_angle = subcarriers - a * k_index_i - b
        return new_one_road_subcarrier_30_angle[index]
