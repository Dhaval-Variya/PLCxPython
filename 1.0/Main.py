#######################################################
#  THIS CODE HAS BEEN OMITTED DUE TO CONFIDENTIALITY  #
#  DO NOT RUN THIS CODE.                              #
#######################################################


import pyautogui
import cv2
import sys
import threading
import time
import datetime
import multiprocessing
import threading

import numpy as np
import json
import os
from csv import writer

from MODBUS import ClientPLC  # NOT REAL LIBRARY NAME
from PyQt5 import QtCore, QtWidgets

from Canvas import ChartCanvas
from PLCAddresses import get_bit
from Settings import SettingWindow
from Count_Bar import Count_Bar


class IO:
    def __init__(self):
        self.ydata = []
        self.typ = None
        self.response = None
        self.bit = None


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("PLC Timing Charts")
        self.setStyleSheet("background-color: #1b1b1b")

        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.canvas = ChartCanvas(self)

        self.main_layout = QtWidgets.QGridLayout(self.main_widget)

        self.setting = SettingWindow(self)
        self.settingbtn = QtWidgets.QPushButton("PLC Settings")
        self.settingbtn.setMinimumWidth(130)
        self.settingbtn.setStyleSheet(
            "background-color: #424242; color:#ffffff")

        self.btn_spacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        # self.record = ScreenRecord(self)
        self.recbtn = QtWidgets.QPushButton("Record")
        self.recbtn.setMinimumWidth(130)
        self.recbtn.setCheckable(True)
        self.recbtn.setStyleSheet("background-color: #424242;color:#ffffff")

        self.horizontal_line = QtWidgets.QFrame()
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontal_line.setLineWidth(2)

        self.count_bar = Count_Bar(self)
        self.count_bar.setStyleSheet("font-size:15pt")

        self.main_layout.addWidget(self.canvas, 1, 0, 1, 3)
        self.main_layout.addWidget(self.settingbtn, 0, 2, 1, 1)
        self.main_layout.addItem(self.btn_spacer, 0, 0, 1, 1)
        self.main_layout.addWidget(self.recbtn, 0, 1, 1, 1)
        self.main_layout.addWidget(self.horizontal_line, 2, 0, 1, 3)
        self.main_layout.addWidget(self.count_bar, 3, 0, 1, 3)
        # self.btn.move(100, 100)
        self.settingbtn.clicked.connect(self.setting.SettingsDiag)
        self.recbtn.clicked.connect(self.button_screenRec)

        self.show()

    def main(self, data_io1, data_io2, data_io3, data_io4, x_data):
        # Need to adjust xdata
        for _plot in [
            self.canvas.io_1,
            self.canvas.io_2,
            self.canvas.io_3,
            self.canvas.io_4,
        ]:
            _plot.xdata = x_data
            _plot.ydata = []
            _plot.count = 0
            _plot.plot_ref = None

        plot = threading.Thread(
            target=update_plots,
            args=(
                self,
                data_io1,
                data_io2,
                data_io3,
                data_io4,
            ),
            daemon=True,
        )
        plot.start()

    def button_screenRec(self):

        start_rec = self.recbtn.isChecked()
        stop_rec = multiprocessing.Value("i", 0)
        rec = multiprocessing.Process(
            target=recorder, args=(stop_rec,), daemon=True)
        if start_rec:
            self.recbtn.setText("Recording..")
            self.recbtn.setStyleSheet("color:#ff5252")
            rec.start()
        else:
            self.recbtn.setText("Record")
            self.recbtn.setStyleSheet(
                "background-color: #424242; color:#ffffff")
            stop_rec.value = 1


def update_plots(self, data_io1, data_io2, data_io3, data_io4):
    while True:
        start = time.time()

        self.canvas.io_1.ydata = data_io1.recv()
        self.canvas.io_2.ydata = data_io2.recv()
        self.canvas.io_3.ydata = data_io3.recv()
        self.canvas.io_4.ydata = data_io4.recv()

        for _io_plot in [
            self.canvas.io_1,
            self.canvas.io_2,
            self.canvas.io_3,
            self.canvas.io_4,
        ]:
            if _io_plot.ydata[-2] < _io_plot.ydata[-1]:
                _io_plot.count += 1
            if _io_plot.plot_ref is None:
                _io_plot.plot_refs = _io_plot.plot(
                    _io_plot.xdata,
                    _io_plot.ydata,
                    _io_plot.color,
                    drawstyle="steps-mid",
                )
                _io_plot.plot_ref = _io_plot.plot_refs[0]
            _io_plot.plot_ref.set_ydata(_io_plot.ydata)

        self.count_bar.update_count(
            self.canvas.io_1.count,
            self.canvas.io_2.count,
            self.canvas.io_3.count,
            self.canvas.io_4.count,
        )
        self.canvas.draw_idle()
        # self.canvas.flush_events()
        elapsed_time = time.time() - start
        # print(self.canvas.io_1.count)


def acquire_signal(data_io1, data_io2, data_io3, data_io4, n_samples):
    io_1 = IO()
    io_2 = IO()
    io_3 = IO()
    io_4 = IO()

    io_1.ydata = [(0) for i in range(len(n_samples))]
    io_2.ydata = [(0) for i in range(len(n_samples))]
    io_3.ydata = [(0) for i in range(len(n_samples))]
    io_4.ydata = [(0) for i in range(len(n_samples))]

    try:
        with open("./plc.json") as f:
            plc = json.load(f)
            ip = plc["ipAddress"]
            io_1.typ, io_1.bit = get_bit(plc["Ports"]["IOport1"])
            io_2.typ, io_2.bit = get_bit(plc["Ports"]["IOport2"])
            io_3.typ, io_3.bit = get_bit(plc["Ports"]["IOport3"])
            io_4.typ, io_4.bit = get_bit(plc["Ports"]["IOport4"])
            clear = plc["clear_flags"]
            plc_client = ClientPLC(ip)
            plc_client.connect()
        while True:
            start = time.time()
            input_data = plc_client.read_discrete_inputs(1024, 32)
            output_data = plc_client.read_coils(1280, 32)
            memory_data = plc_client.read_coils(2048, 100)

            for _io in [io_1, io_2, io_3, io_4]:
                _io.response = process_data(
                    input_data, output_data, memory_data)

                _io.ydata = _io.ydata[1:] + [_io.response]
                _io.log_val = str(f"{_io.typ}{_io.bit}:{_io.response}")

            try:
                data_io1.send(io_1.ydata)
                data_io2.send(io_2.ydata)
                data_io3.send(io_3.ydata)
                data_io4.send(io_4.ydata)
            except:
                err = "Unable to send data for plot update"

            elapsed_time = time.time() - start
            remaining_time = 0.04 - elapsed_time
            err = "No error"
            if remaining_time > 0:
                time.sleep(remaining_time)
            else:
                err = "Warning: Acquisition rate is above 40ms"
                # print(err)
            msg = str(f"Current acquisition rate is: {elapsed_time}seconds")
            logger(
                [
                    datetime.datetime.now().strftime("%H:%M:%S.%f"),
                    msg,
                    io_1.log_val,
                    io_2.log_val,
                    io_3.log_val,
                    io_4.log_val,
                    err,
                ]
            )

    except:
        err = f"Unable to connect to PLC."
        logger(
            [datetime.datetime.now().strftime("%H:%M:%S.%f"),
             "inf", 0, 0, 0, 0, err]
        )


def logger(str):
    folder = "Logs"
    today = datetime.datetime.now()
    filename = (today.strftime("%d%m%Y")) + ".csv"

    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.isfile(os.path.join(folder, filename)):
        with open(os.path.join(folder, filename), "a+", newline="") as file:
            csv_writer = writer(file)
            csv_writer.writerow(
                [
                    "Time",
                    "Acqusition rate",
                    "IO Port1",
                    "IO Port2",
                    "IO Port3",
                    "IO Port4",
                    "Error",
                ]
            )
    with open(os.path.join(folder, filename), "a+", newline="") as file:
        csv_writer = writer(file)
        csv_writer.writerow(str)


def recorder(stop_rec):
    folder = "Recordings"
    today = datetime.datetime.now()
    filename = (today.strftime("%Y_%m_%d %H%M%S")) + ".avi"
    resolution = pyautogui.size()
    codec = cv2.VideoWriter_fourcc(*"XVID")

    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)

    fps = 25
    vid_writer = cv2.VideoWriter(filepath, codec, fps, resolution)
    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        vid_writer.write(frame)
        if stop_rec.value == 1:
            break
    vid_writer.release()


if __name__ == "__main__":

    multiprocessing.freeze_support()
    app = QtWidgets.QApplication(sys.argv)
    parent_io1, child_io1 = multiprocessing.Pipe()
    parent_io2, child_io2 = multiprocessing.Pipe()
    parent_io3, child_io3 = multiprocessing.Pipe()
    parent_io4, child_io4 = multiprocessing.Pipe()
    n_samples = np.linspace(0, 249, 250)
    x_data = [((len(n_samples) - i) * 0.04) for i in range(len(n_samples))]

    if os.path.exists("./plc.json"):
        pass
    else:
        data = {}
        Ports = {}
        data["Title"] = "Please Insert Title"
        data["ipAddress"] = "10.255.0.2"
        Ports["IOport1"] = "X0"
        Ports["IOport2"] = "X0"
        Ports["IOport3"] = "X0"
        Ports["IOport4"] = "X0"
        data["Ports"] = Ports
        data["clear_flags"] = False
        with open("./plc.json", "w") as f:
            json.dump(data, f, indent=4)

    w = MainWindow()

    acquire = multiprocessing.Process(
        name="Data Acquisition",
        target=acquire_signal,
        args=(parent_io1, parent_io2, parent_io3, parent_io4, n_samples),
        daemon=True,
    )
    acquire.start()
    w.main(child_io1, child_io2, child_io3, child_io4, x_data)

    app.exec_()
