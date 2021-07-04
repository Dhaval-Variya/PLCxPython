from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication
import sys


class Count_Bar(QWidget):
    def __init__(self, parent=None):
        super(Count_Bar, self).__init__(parent)
        self.grid = QHBoxLayout(self)
        self.count_io1 = QLabel()
        # font1 = self.count_io1.font()
        # font1.setPointSize(1000)
        self.count_io2 = QLabel()
        self.count_io3 = QLabel()
        self.count_io4 = QLabel()

        self.grid.addWidget(self.count_io1)
        self.grid.addWidget(self.count_io2)
        self.grid.addWidget(self.count_io3)
        self.grid.addWidget(self.count_io4)

        self.count_io1.setStyleSheet("color:#00acc1")
        self.count_io2.setStyleSheet("color:#ff5722")
        self.count_io3.setStyleSheet("color:#43a047")
        self.count_io4.setStyleSheet("color:#e040fb")

    def update_count(self, cnt1, cnt2, cnt3, cnt4):
        self.count_io1.setText(str(f"Count: {cnt1}"))
        self.count_io2.setText(str(f"Count: {cnt2}"))
        self.count_io3.setText(str(f"Count: {cnt3}"))
        self.count_io4.setText(str(f"Count: {cnt4}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    canvas = Count_Bar()
    sys.exit(app.exec_())
