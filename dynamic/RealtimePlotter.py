'''
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
'''
import threading
from time import sleep, clock

import matplotlib

matplotlib.use('Qt5Agg')
import matplotlib.animation as animation
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtWidgets


class RealtimePlotter(object):
    '''
    Real-time scrolling multi-plot over time.  Your data-acquisition code should run on its own thread,
    to prevent blocking / slowdown.
    '''
    ani = None

    def __init__(self, size=200,
                 window_name=None, styles=None, ylabels=None, yticks=[], legend=[], interval_msec=10):
        '''
        Initializes a multi-plot with specified Y-axis limits as a list of pairs; e.g.,
        [(-1,+1), (0.,5)].  Optional parameters are:

        size             size of display (X axis) in arbitrary time steps
        window_name      name to display at the top of the figure
        styles           plot styles (e.g., 'b-', 'r.'; default='b-')
        yticks           Y-axis tick / grid positions
        legends          list of legends for each subplot
        interval_msec    animation update in milliseconds

        For overlaying plots, use a tuple for styles; e.g., styles=[('r','g'), 'b']
        '''
        # MyMplCanvas.__init__(self)
        # Row count is provided by Y-axis limits

        # Bozo filters
        # styles = self._check_param(nrows, styles, 'styles', 'b-')
        # ylabels = self._check_param(nrows, ylabels, 'ylabels', '')
        # yticks = self._check_param(nrows, yticks, 'yticks', [])
        # self.legends = self._check_param(nrows, legends, 'legends', [])
        self.fig = Figure(figsize=(5, 4), dpi=100)
        # X values are arbitrary ascending; Y is initially zero
        self.x = np.arange(0, size)
        y = np.zeros(size)
        self.flag = False
        self.pause = False
        self.last_line = None
        self.axes = None

        self.axes = self.fig.add_subplot(111)
        if window_name:
            self.fig.canvas.set_window_title(window_name)

        # Create lines
        self.lines = []
        style = styles
        ax = self.axes
        # legend = [[]]
        stylesForRow = style if type(style) == tuple else [style]
        for k in range(len(stylesForRow)):
            label = legend[k] if legend and len(legend) > 0 else ''
            self.lines.append(ax.plot(self.x, y, stylesForRow[k], animated=True)[0])
        if legend is not None and len(legend) > 0:
            ax.legend()

        # Add properties as specified
        ax.set_ylabel(ylabels)

        # Set axis limits
        ax.set_xlim((0, size))
        # [ax.set_ylim(ylim) for ax, ylim in zip(self.axes, ylims)]

        # Set ticks and gridlines
        ax.yaxis.set_ticks(yticks)
        ax.yaxis.grid(True)

        # XXX Hide X axis ticks and labels for now
        ax.xaxis.set_visible(False)
        # Allow interval specification
        self.interval_msec = interval_msec

    def start(self):

        """
        Starts the realtime plotter.
        """

        if RealtimePlotter.ani is None:
            RealtimePlotter.ani = animation.FuncAnimation(self.fig, self._animate, interval=self.interval_msec,
                                                          blit=True)
        else:
            pass

    def getValues(self):

        """
        Override this method to return actual Y values at current time.
        """

        return None

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

    def _animate(self, t):
        if self.pause is True:
            return self.last_line
        values = self.getValues()
        yvals = values
        RealtimePlotter.rolly(self.lines[0], yvals)
        self.last_line = self.lines
        return self.lines


def _update():
    from time import sleep
    while True:
        sleep(.001)
