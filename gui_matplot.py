import flightradar24
import sys
import matplotlib
matplotlib.use("Qt5Agg")
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QSizePolicy, QWidget, QMainWindow, QMenu, QVBoxLayout, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)
import flight_basic_info

idinp = input(str("enter ID "))
icao24inp = input(str("enter icao24: "))
flight = flight_basic_info.flight_path_info(idinp, icao24inp)
flight.run_down_info()


#This gui_matplot file is for plotting 

#flight_basic_info.run_down_info()

class MyMatPlotCanvas(FigureCanvas):
    #template as to hold your map application up
    def __init__(self, parent=None, width=10, height=7, dpi=300):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes.plot()
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class StaticMPLCanvas(MyMatPlotCanvas):
    #This is what is being graphed on the gui
    def update_figure(self, f):
        self.axes.cla()
        t = np.arange(0.0,30.0, 0.01)
        s = np.sin(f*np.pi*t)
        self.axes.plot(t,s)
        self.draw()

class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #menu bar
        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.close, Qt.CTRL + Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.main_widget = QWidget()
        layout = QVBoxLayout(self.main_widget)

        self.input_flightcode = QLineEdit(self)

        sc = StaticMPLCanvas(self.main_widget)

        #self.spinbox value changed is connected to the update figure
        #method from the static class
        #we can use this that way whatever code is inputted into the spinbox
        #it will graph the new flight path function.

        #self.input_flightcode.textChanged.connect(sc.update_figure)
        #sc.update_figure(self.input_flightcode.value())

        layout.addWidget(self.input_flightcode)
        layout.addWidget(sc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.setWindowTitle("Flight Tracker Using Matplotlib")
    win.show()
    sys.exit(app.exec_())
        
