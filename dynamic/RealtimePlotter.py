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

import matplotlib
import matplotlib.animation as animation
import numpy as np
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class RealtimePlotter(object):
    """
    Real-time scrolling multi-plot over time.  Your data-acquisition code should run on its own thread,
    to prevent blocking / slowdown.
    """
    ani = None

    def __init__(self, size=200, window_name=None,
                 styles=None, xlabels=None, ylabels=None,
                 yticks=None, legend=None, interval=1):
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

        self.fig = Figure(figsize=(10, 9), dpi=100, tight_layout=True)
        # X values are arbitrary ascending; Y is initially zero
        self.x = np.arange(0, size)
        y = np.zeros(size)
        self.pause_flag = False
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
        styles_for_row = style if type(style) == tuple else [style]
        for k in range(len(styles_for_row)):
            self.lines.append(ax.plot(self.x, y, styles_for_row[k], animated=True)[0])
        if legend is not None and len(legend) > 0:
            ax.legend()

        # Add properties as specified
        ax.set_xlabel(xlabels, fontsize=15)
        ax.set_ylabel(ylabels, fontsize=15)

        # Set axis limits
        ax.set_xlim(0, size)
        # [ax.set_ylim(ylim) for ax, ylim in zip(self.axes, ylims)]

        # Set ticks and gridlines
        ax.yaxis.set_ticks(yticks)
        ax.yaxis.grid(True)

        # XXX Hide X axis ticks and labels for now
        # ax.xaxis.set_visible(False)
        # Allow interval specification
        self.interval_msec = interval

    def start(self):

        if RealtimePlotter.ani is None:
            RealtimePlotter.ani = animation.FuncAnimation(self.fig, self._animate, interval=self.interval_msec,
                                                          blit=True)
        else:
            RealtimePlotter.ani.event_source.start()

    @staticmethod
    def puase():
        RealtimePlotter.ani.event_source.stop()

    def get_values(self):

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

    def _animate(self, _):
        if self.pause_flag is True:
            return self.last_line
        values = self.get_values()
        yvals = values
        RealtimePlotter.rolly(self.lines[0], yvals)
        self.last_line = self.lines
        return self.lines


def _update():
    from time import sleep
    while True:
        sleep(.001)
