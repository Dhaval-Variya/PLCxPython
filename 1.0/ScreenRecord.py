from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QApplication,
)
import sys
import multiprocessing
import pyautogui
import cv2
import numpy as np


class ScreenRecord(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        resolution = pyautogui.size()
        codec = cv2.VideoWriter_fourcc(*"XVID")
        filename = "Recording.avi"
        fps = 20.0
        self.vid = cv2.VideoWriter(filename, codec, fps, resolution)
        # self.initUI()

    def ScreenRec(self, checked):

        global stoprec
        rec = multiprocessing.Process(target=self.loop, args=(self,), daemon=True)
        if checked:
            stoprec = False
            rec.start()
        else:
            stoprec = True
            self.vid.release()

    def loop(self):
        while True:
            img = pyautogui.screenshot()
            self.frame = np.array(img)
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.vid.write(self.frame)
            if stoprec:
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ScreenRecord()
    sys.exit(app.exec_())