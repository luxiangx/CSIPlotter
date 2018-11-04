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

    def __init__(self):
        """
        Initializes a multi-plot with specified Y-axis limits as a list of pairs; e.g.,
        [(-1,+1), (0.,5)].  Optional parameters are:

        size             size of display (X axis) in arbitrary time steps
        window_name      name to display at the top of the figure
        styles           plot styles (e.g., 'b-', 'r.'; default='b-')
        yticks           Y-axis tick / grid positions
        legends          list of legends for each subplot
        interval_msec    animation update in milliseconds

        For overlaying plots, use a tuple for styles; e.g., styles=[('r','g'), 'b']
        """
        self.size = 200
        self.styles = 'r-'
        self.xlabels = "Time"
        self.ylabels = "Amplitude"
        self.yticks = (0, 35, 70)
        self.legend = None
        self.interval = 1
        self.tx = 'A'
        self.rx = 'A'
        self.subcarrier_no = '1'
        self.mode = '子载波显示'
        self.data = '幅值'
        self.offset = 0
        self.last_value = None
        self.filename = ""
        self.fig = Figure(figsize=(10, 20), dpi=100, tight_layout=True)
        # X values are arbitrary ascending; Y is initially zero
        self.x = np.arange(0, self.size)
        y = np.zeros(self.size)
        self.pause_flag = False
        self.last_line = None
        self.axes = None

        self.axes = self.fig.add_subplot(111)

        # Create lines
        self.lines = []
        style = self.styles
        ax = self.axes
        # legend = [[]]
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
        # [ax.set_ylim(ylim) for ax, ylim in zip(self.axes, ylims)]

        # Set ticks and gridlines
        ax.yaxis.set_ticks(self.yticks)
        ax.yaxis.grid(True)

        # XXX Hide X axis ticks and labels for now
        # ax.xaxis.set_visible(False)
        # Allow interval specification
        self.interval_msec = self.interval

    def start(self):
        t = threading.Thread(target=self.log())
        t.start()
        self.fig.canvas.flush_events()
        if RealtimePlotter.ani is None:
            RealtimePlotter.ani = animation.FuncAnimation(self.fig, self.animate, interval=self.interval_msec,
                                                          blit=True)
        else:
            RealtimePlotter.ani.event_source.start()

    @staticmethod
    def puase():
        RealtimePlotter.ani.event_source.stop()

    def get_values(self):
        r = self.get_values_by_mode()
        return r

    def _axis_check(self, axid):

        nrows = len(self.lines)
        if axid < 0 or axid >= nrows:
            raise Exception('Axis index must be in [0,%d)' % nrows)

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
            "; sudo /home/luxiang/linux-80211n-csitool-supplementary/netlink/log_to_file_1 " +
            self.filename.split("/")[-1] + "&",
            shell=True)

    def get_single_subcarrier_amplitude_value(self):
        file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
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
        file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[len(file_data) - 1]
            csi = load_csi_real_time_data.get_scale_csi(csi_entry)
            return get_true_phase(csi[ord(self.tx) - ord('A')][ord(self.rx) - ord('A')][:], int(self.subcarrier_no))
        else:
            return self.last_value

    def get_antenna_pair_phase_value(self):
        pass

    def get_all_data_phase_value(self):
        pass

    def get_values_by_mode(self):

        if self.data == '幅值':
            self.yticks = (-3.14, 0, +3.14)
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
