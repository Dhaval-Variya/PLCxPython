import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import os
import json

matplotlib.use("Qt5Agg")


class ChartCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        """
        Canvas containing individual charts for each port selected. Please use a maximum of 4 charts

        ------

        Parameters:
        --------
            ports = PLC Ports selected to be used for timing charts

        """
        plt.ion()
        fig = Figure(figsize=(19, 10), dpi=100, constrained_layout=True)
        fig.set_facecolor("#1B1B1B")

        self.io_1 = fig.add_subplot(411)
        self.io_2 = fig.add_subplot(412, sharex=self.io_1)
        self.io_3 = fig.add_subplot(413, sharex=self.io_1)
        self.io_4 = fig.add_subplot(414, sharex=self.io_1)

        with open("./plc.json") as f:
            plc = json.load(f)
            title = plc["Title"]
            self.io_1.name = plc["Ports"]["IOport1"]
            self.io_2.name = plc["Ports"]["IOport2"]
            self.io_3.name = plc["Ports"]["IOport3"]
            self.io_4.name = plc["Ports"]["IOport4"]

        self.io_1.color = "#00acc1"
        self.io_2.color = "#ff5722"
        self.io_3.color = "#43a047"
        self.io_4.color = "#e040fb"

        # fig.suptitle(title, color="#FFFFFF")
        # fig.patch.set_facecolor("#1b1b1b")

        for _plot in [self.io_1, self.io_2, self.io_3, self.io_4]:
            _plot.set_ylim(-0.1, 1.1)
            _plot.set_yticks([0, 1])
            _plot.set_xlim(10, 0)
            _plot.grid(color="#FFFFFF", linestyle="--", linewidth=0.5, axis="y")
            _plot.patch.set_facecolor("#424242")
            _plot.get_xaxis().set_visible(False)
            _plot.tick_params(axis="x", colors="#FFFFFF")
            _plot.tick_params(axis="y", colors="#FFFFFF")
            _plot.set_ylabel(
                _plot.name, color=_plot.color, rotation="horizontal", ha="right"
            )

            for _side in ["top", "left", "right", "bottom"]:
                _plot.spines[_side].set_color("#FFFFFF")

        self.io_1.spines["bottom"].set_visible(False)
        self.io_2.spines["top"].set_visible(False)
        self.io_2.spines["bottom"].set_visible(False)
        self.io_3.spines["top"].set_visible(False)
        self.io_3.spines["bottom"].set_visible(False)
        self.io_4.spines["top"].set_visible(False)

        self.io_4.get_xaxis().set_visible(True)
        self.io_4.set_xlabel("Time (seconds)", color="#FFFFFF")

        # fig.tight_layout()
        # fig.subplots_adjust(hspace=0)
        fig.set_constrained_layout_pads(h_pad=0, hspace=0)
        super(ChartCanvas, self).__init__(fig)


if __name__ == "__main__":
    canvas = ChartCanvas()
