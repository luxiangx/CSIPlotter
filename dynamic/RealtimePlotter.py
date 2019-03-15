# -*- coding: utf-8 -*-

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
    ani = None
    error_no = 0
    """
    1: tx error, don't have antenna B
    2: tx error, don't have antenna C
    3: tx error, should select antenna B
    4: tx error, should select antenna C
    """

    def __init__(self, ui):
        self.ui = ui
        self.size = 200
        self.styles = 'r-'
        self.xlabels = "Time"
        self.ylabels = "Amplitude"
        self.yticks = (0, 35, 70)
        self.legend = None
        self.interval_msec = 10
        self.tx = 0
        self.rx = 0
        self.subcarrier_no = 0
        self.mode = 'subcarrier'
        self.data = 'amplitude'
        self.offset = 0
        self.last_value = None
        self.last_plot_data = None
        self.filename = ""
        self.fig = Figure(figsize=(10, 20), dpi=100, tight_layout=True)
        # X values are arbitrary ascending; Y is initially zero
        self.x = np.arange(0, self.size)
        y = np.zeros(self.size)
        self.start_flag = False
        self.check_error_flag = True
        self.axes = self.fig.add_subplot(111)

        # Create lines
        self.lines = []
        self.antenna_image = np.zeros((30, self.size))
        self.antenna_images = []
        self.all_image = None
        self.all_images = []
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
        ax.set_xlim(0, self.size - 0.5)

        # Set ticks and gridlines
        ax.yaxis.set_ticks(self.yticks)
        ax.yaxis.grid(True)
        ax.yaxis.set_visible(True)

    def start(self):
        t = threading.Thread(target=self.log())
        t.start()
        v_min, v_max = 0, 0
        if self.data == 'phase':
            v_min = -3.14
            v_max = 3.14
        elif self.data == 'amplitude':
            v_min = 0
            v_max = 70
        if self.mode == "subcarrier":

            RealtimePlotter.ani = animation.FuncAnimation(self.fig, self.animate_subcarrier,
                                                          blit=True, interval=self.interval_msec)
        elif self.mode == "rssi":
            RealtimePlotter.ani = animation.FuncAnimation(self.fig, self.animate_rssi,
                                                          blit=True, interval=self.interval_msec)
        elif self.mode == "antenna pair":
            self.antenna_images.append(self.axes.imshow(self.antenna_image, cmap='jet', aspect='auto',
                                                        vmin=v_min, vmax=v_max, animated=True))
            RealtimePlotter.ani = animation.FuncAnimation(self.fig, self.animate_antenna,
                                                          blit=True, interval=self.interval_msec)
        elif self.mode == "all csi":
            if self.tx == 0:
                self.all_image = np.zeros((90, self.size))
            elif self.tx == 1:
                self.all_image = np.zeros((180, self.size))
            else:
                self.all_image = np.zeros((270, self.size))
            self.all_images.append(self.axes.imshow(self.all_image, cmap='jet', aspect='auto',
                                                    vmin=v_min, vmax=v_max, animated=True))
            RealtimePlotter.ani = animation.FuncAnimation(self.fig, self.animate_all,
                                                          blit=True, interval=self.interval_msec)

    def get_values(self):
        if self.start_flag:
            r = self.get_values_by_mode()
            return r
        return None

    def check_error(self):

        if RealtimePlotter.error_no == 1:
            self.stop_log()
            self.ui.msg_text.append("<font color = 'red'>-> Do not have TX B!")
        elif RealtimePlotter.error_no == 2:
            self.stop_log()
            self.ui.msg_text.append("<font color = 'red'>-> Do not have TX C!")
        elif RealtimePlotter.error_no == 3:
            self.stop_log()
            self.ui.msg_text.append("<font color = 'red'>-> Please select TX B!")
        elif RealtimePlotter.error_no == 4:
            self.stop_log()
            self.ui.msg_text.append("<font color = 'red'>-> Please select TX C!")

    def get_values_by_mode(self):
        if self.mode == 'rssi':
            self.last_plot_data = self.get_rssi_value()
            return self.last_plot_data
        elif self.mode == 'subcarrier':
            if self.data == 'amplitude':
                self.last_plot_data = self.get_single_subcarrier_amplitude_value()
                if self.check_error_flag:
                    self.check_error_flag = False
                    self.check_error()
                return self.last_plot_data
            elif self.data == 'phase':
                self.last_plot_data = self.get_single_subcarrier_phase_value()
                if self.check_error_flag:
                    self.check_error_flag = False
                    self.check_error()
                return self.last_plot_data
        elif self.mode == 'antenna pair':
            if self.data == 'amplitude':
                self.last_plot_data = self.get_antenna_pair_amplitude_value()
                if self.check_error_flag:
                    self.check_error_flag = False
                    self.check_error()
                return self.last_plot_data
            elif self.data == 'phase':
                self.last_plot_data = self.get_antenna_pair_phase_value()
                if self.check_error_flag:
                    self.check_error_flag = False
                    self.check_error()
                return self.last_plot_data
        elif self.mode == 'all csi':
            if self.data == 'amplitude':
                self.last_plot_data = self.get_all_data_amplitude_value()
                if self.check_error_flag:
                    self.check_error_flag = False
                    self.check_error()
                return self.last_plot_data
            elif self.data == 'phase':
                self.last_plot_data = self.get_all_data_phase_value()
                if self.check_error_flag:
                    self.check_error_flag = False
                    self.check_error()
                return self.last_plot_data

    def animate_rssi(self, _):
        values = self.get_values()
        RealtimePlotter.roll_y_value(self.lines[0], values)
        self.last_plot_data = self.lines
        return self.lines

    def animate_subcarrier(self, _):
        values = self.get_values()
        RealtimePlotter.roll_y_value(self.lines[0], values)
        self.last_plot_data = self.lines
        return self.lines

    def animate_antenna(self, _):
        values = self.get_values()
        RealtimePlotter.roll_image(self.antenna_images[0], values)
        self.last_plot_data = self.antenna_images
        return self.last_plot_data

    def animate_all(self, _):
        values = self.get_values()
        RealtimePlotter.roll_image(self.all_images[0], values)
        self.last_plot_data = self.all_images
        return self.last_plot_data

    def log(self):
        subprocess.call(
            "cd " + self.filename[:self.filename.find(self.filename.split("/")[-1])] +
            "; sudo ~/linux-80211n-csitool-supplementary/netlink/log_to_file " +
            self.filename.split("/")[-1] + "&", shell=True)

    def stop_log(self):
        # find the log process, and kill it.
        os.system("sudo kill -s 9 `ps -ef|grep '../netlink/log_to_file'|grep -v sudo|grep -v grep|awk '{print $2}'`")
        self.ui.add_msg('-> Stop showing!')
        self.pause()
        self.start_flag = False
        self.reset()

    def get_rssi_value(self):
        file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[len(file_data) - 1]
            self.last_value = load_csi_real_time_data.get_total_rss(csi_entry)
        return self.last_value

    def get_single_subcarrier_amplitude_value(self):
        file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[len(file_data) - 1]
            csi = load_csi_real_time_data.get_scale_csi(csi_entry)
            try:
                self.last_value = abs(np.squeeze(csi[self.tx][self.rx][self.subcarrier_no]))
            except IndexError:
                RealtimePlotter.error_no = 1 if self.tx == 1 else 2
        return self.last_value

    def get_antenna_pair_amplitude_value(self):
        file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[len(file_data) - 1]
            csi = load_csi_real_time_data.get_scale_csi(csi_entry)
            try:
                self.last_value = abs(np.squeeze(csi[self.tx][self.rx][:]))
            except IndexError:
                RealtimePlotter.error_no = 1 if self.tx == 1 else 2
        return self.last_value

    def get_all_data_amplitude_value(self):
        file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[len(file_data) - 1]
            csi = load_csi_real_time_data.get_scale_csi(csi_entry)
            csi_amplitude = abs(np.squeeze(csi))
            n_size = np.size(csi_amplitude)
            n_c = 90 * (self.tx + 1)
            if n_size == n_c:
                self.last_value = np.reshape(csi_amplitude, n_size)
            elif n_size < n_c:
                RealtimePlotter.error_no = 1 if self.tx == 1 else 2
            elif n_size > n_c:
                RealtimePlotter.error_no = 3 if n_size // 90 == 2 else 4
        return self.last_value

    def get_single_subcarrier_phase_value(self):
        file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[len(file_data) - 1]
            csi = load_csi_real_time_data.get_scale_csi(csi_entry)
            try:
                self.last_value = self.get_true_phase(csi[self.tx][self.rx][:], self.subcarrier_no)
            except IndexError:
                RealtimePlotter.error_no = 1 if self.tx == 1 else 2
        return self.last_value

    def get_antenna_pair_phase_value(self):
        file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[len(file_data) - 1]
            csi = load_csi_real_time_data.get_scale_csi(csi_entry)
            try:
                self.last_value = self.get_true_phase(csi[self.tx][self.rx][:], -1)
            except IndexError:
                RealtimePlotter.error_no = 1 if self.tx == 1 else 2
        return self.last_value

    def get_all_data_phase_value(self):
        file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[len(file_data) - 1]
            csi = load_csi_real_time_data.get_scale_csi(csi_entry)
            csi_phase = self.get_true_phase(csi, -2)
            n_size = np.size(csi_phase)
            n_c = 90 * (self.tx + 1)
            if n_size == n_c:
                self.last_value = np.reshape(csi_phase, n_size)
            elif n_size < n_c:
                RealtimePlotter.error_no = 1 if self.tx == 1 else 2
            elif n_size > n_c:
                RealtimePlotter.error_no = 3 if n_size // 90 == 2 else 4
        return self.last_value

    @classmethod
    def roll_image(cls, image, newval):
        t = image.get_array()
        t = np.roll(t, -1, axis=1)
        t[:, -1] = newval
        image.set_array(t)

    @classmethod
    def roll_y_value(cls, line, newval):
        data = line.get_ydata(line)
        data = np.roll(data, -1)
        data[-1] = newval
        line.set_ydata(data)

    @staticmethod
    def pause():
        RealtimePlotter.ani.event_source.stop()

    @staticmethod
    def reset():
        RealtimePlotter.error_no = 0

    @staticmethod
    def get_true_phase(csi, index):
        """
        :param csi: csi data
        :param index: if index is -1 return all true phase,
         else if index is 0 return a pair antenna,
         else return the tx-rx-subcarrier number true phase.
        :return: true phase data
        """
        import math
        csi_phase = np.angle(csi)
        temp = np.zeros(30)
        recycle = 0
        k_index_i = np.array([-28, -26, -24, -22, -20, -18, -16, -14, -12, -10, -8, -6, -4, -2, -1,
                              1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 28]).T
        # k_index_i = np.array([-58, -54, -50, -46, -42, -38, -34, -30, -26, -22, -18, -14, -10, -6, -2,
        #                       2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58]).T
        if index >= -1:
            temp[0] = csi_phase[0]
            for t_i in range(1, 30):
                if csi_phase[t_i] - csi_phase[t_i - 1] > math.pi:
                    recycle = recycle + 1
                temp[t_i] = csi_phase[t_i] - recycle * 2 * math.pi
            csi_phase = temp.T
            a = (csi_phase[29] - csi_phase[0]) / 56
            b = np.mean(csi_phase)
            true_phase = csi_phase - a * k_index_i - b
            if index == -1:
                return true_phase  # 30 subcarriers
            else:
                return true_phase[index]  # 1 subcarrier
        else:
            [tx, rx, s] = np.shape(csi_phase)
            true_phase = np.zeros((1, tx * rx * s))
            for i in range(tx):
                for j in range(rx):
                    temp[0] = csi_phase[i][j][0]
                    for t_i in range(1, 30):
                        if csi_phase[i][j][t_i] - csi_phase[i][j][t_i - 1] > math.pi:
                            recycle = recycle + 1
                        temp[t_i] = csi_phase[i][j][t_i] - recycle * 2 * math.pi
                    csi_phase[i][j] = temp.T
                    a = (csi_phase[i][j][29] - csi_phase[i][j][0]) / 56
                    b = np.mean(csi_phase[i][j])
                    true_phase[0, (90 * i + 30 * j):(90 * i + 30 * (j + 1))] = csi_phase[i][j] - a * k_index_i - b
            return true_phase
