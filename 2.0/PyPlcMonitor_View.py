# Import the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import (
    QWidget,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
)
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


# Create a subclass of QMainWindow to setup the calculator's GUI
class PyPlcMonitorUi(QMainWindow):
    """PyPLC Monitor's View (GUI)."""

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle("PyPLC Monitoring System")
        # Set the central widget
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet(
            " background-color: #424242; color:white; font-size:11pt; QPushButton { border: 1px solid white }"
        )
        self.main_grid = QGridLayout(self.main_widget)

        self._create_elements()

    def _create_elements(self):
        """Create basic elements present in the UI.
        ----
        - Settings Button
        - Recording Button
        - Horizontal Divider
        - Horizontal Spacer
        - Counter Labels
        - Matplotlib Charts
        """

        ##### SETTINGS BUTTON #####
        self.settings_btn = QPushButton("PLC Settings")
        self.settings_btn.setMinimumWidth(130)

        ##### RECORDING BUTTON #####
        self.recording_btn = QPushButton("Record Screen")
        self.recording_btn.setMinimumWidth(130)
        self.recording_btn.setCheckable(True)

        ##### HORIZONTAL DIVIDER #####
        self.horizontal_line = QFrame()
        self.horizontal_line.setFrameShape(QFrame.HLine)
        self.horizontal_line.setFrameShadow(QFrame.Sunken)
        self.horizontal_line.setLineWidth(2)

        ##### HORIZONTAL SPACER #####
        self.btn_spacer = QSpacerItem(
            20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        ##### COUNTER LABELS #####
        self.counter_labels = Counter(parent=self.main_grid)
        self.counter_labels.setStyleSheet("font-size:14pt")

        ##### CHARTS #####
        self.charts = Charts(self)

        ##### ADD ELEMENTS TO LAYOUT #####

        self.main_grid.addWidget(self.settings_btn, 0, 2, 1, 1)
        self.main_grid.addWidget(self.recording_btn, 0, 1, 1, 1)
        self.main_grid.addItem(self.btn_spacer, 0, 0, 1, 1)
        self.main_grid.addWidget(self.charts, 1, 0, 1, 3)
        self.main_grid.addWidget(self.horizontal_line, 2, 0, 1, 3)
        self.main_grid.addWidget(self.counter_labels, 3, 0, 1, 3)


class Counter(QWidget):
    """Class creating counter labels."""

    def __init__(self, parent=None):
        """Label initializer."""
        super(Counter, self).__init__()
        self.grid = QHBoxLayout(self)
        self.counter_1 = QLabel()
        self.counter_2 = QLabel()
        self.counter_3 = QLabel()
        self.counter_4 = QLabel()

        self.grid.addWidget(self.counter_1)
        self.grid.addWidget(self.counter_2)
        self.grid.addWidget(self.counter_3)
        self.grid.addWidget(self.counter_4)

        # font1 = self.count_io1.font()
        # font1.setPointSize(1000)

        # self.count_io1.setStyleSheet("color:#00acc1")
        # self.count_io2.setStyleSheet("color:#ff5722")
        # self.count_io3.setStyleSheet("color:#43a047")
        # self.count_io4.setStyleSheet("color:#e040fb")
        self.counter_1.setText("Count: 000")
        self.counter_2.setText("Count: 000")
        self.counter_3.setText("Count: 000")
        self.counter_4.setText("Count: 000")


class Charts(FigureCanvasQTAgg):
    """Class creating Matplotlib charts."""

    def __init__(self, parent=None):
        """Chart initializer."""
        matplotlib.use("Qt5Agg")
        plt.style.use("./PLC_GUI.mplstyle")
        fig = Figure(figsize=(16, 9), dpi=100)
        self.chart_1 = fig.add_subplot(411)
        self.chart_2 = fig.add_subplot(412, sharex=self.chart_1)
        self.chart_3 = fig.add_subplot(413, sharex=self.chart_1)
        self.chart_4 = fig.add_subplot(414, sharex=self.chart_1)

        for _plot in [self.chart_1, self.chart_2, self.chart_3, self.chart_4]:
            _plot.set_ylim(-0.1, 1.1)
            _plot.set_yticks([0, 1])
            _plot.set_xlim(10, 0)

        self.chart_1.spines["bottom"].set_visible(False)
        self.chart_2.spines["top"].set_visible(False)
        self.chart_2.spines["bottom"].set_visible(False)
        self.chart_3.spines["top"].set_visible(False)
        self.chart_3.spines["bottom"].set_visible(False)
        self.chart_4.spines["top"].set_visible(False)
        self.chart_4.get_xaxis().set_ticks_position("bottom")
        self.chart_4.set_xlabel("Time (seconds)", color="#FFFFFF")

        super(Charts, self).__init__(fig)
