# -----------------------------------------------------------------------------
#
#
# -----------------------------------------------------------------------------
import sys
import pyqtgraph as pg
from pyqtgraph.ptime import time
from pyqtgraph.Qt import QtCore, QtGui
from hardware import Hardware

# -----------------------------------------------------------------------------
hw = None
MINIMUM_WIDTH = 230

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class UIClass(QtGui.QMainWindow):

    # -------------------------------------------------------------------------
    def __init__(self):

        # ---------------------------------------------------------------------
        #
        # ---------------------------------------------------------------------
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Test application')

        # ---------------------------------------------------------------------
        #
        # ---------------------------------------------------------------------
        parentWidget = QtGui.QWidget()
        vbox_gr = QtGui.QGridLayout()
        vbox_ui = QtGui.QVBoxLayout()
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox_ui)
        hbox.addLayout(vbox_gr)
        parentWidget.setLayout(hbox)
        self.setCentralWidget(parentWidget)

        # ---------------------------------------------------------------------
        #
        # ---------------------------------------------------------------------
        logoGBox = QtGui.QGroupBox()
        logoGBoxLayout = QtGui.QGridLayout()
        logoGBox.setLayout(logoGBoxLayout)
        logoGBox.setMaximumWidth(MINIMUM_WIDTH)
        logoGBox.setMinimumWidth(MINIMUM_WIDTH)
        # ---------------------------------------------------------------------
        label = QtGui.QLabel()
        pixmap = QtGui.QPixmap('logo.png')
        label.setPixmap(pixmap)
        logoGBoxLayout.addWidget(label)

        # ---------------------------------------------------------------------
        #
        # ---------------------------------------------------------------------
        infoGBox = QtGui.QGroupBox("General info")
        infoGBoxLayout = QtGui.QGridLayout()
        infoGBox.setLayout(infoGBoxLayout)
        infoGBox.setMinimumWidth(MINIMUM_WIDTH)
        infoGBox.setMaximumWidth(MINIMUM_WIDTH)
        # ---------------------------------------------------------------------
        self.val0_label = QtGui.QLabel("...")
        infoGBoxLayout.addWidget(QtGui.QLabel("Val0: "),0,0)
        infoGBoxLayout.addWidget(self.val0_label,0,1,1,7)
        # ---------------------------------------------------------------------
        self.val1_label = QtGui.QLabel("...")
        infoGBoxLayout.addWidget(QtGui.QLabel("Val1: "),1,0)
        infoGBoxLayout.addWidget(self.val1_label,1,1,1,7)
        # ---------------------------------------------------------------------
        self.val2_label = QtGui.QLabel("...")
        infoGBoxLayout.addWidget(QtGui.QLabel("Val2: "),2,0)
        infoGBoxLayout.addWidget(self.val2_label,2,1,1,7)
        # ---------------------------------------------------------------------
        resetGraphButton = QtGui.QPushButton("Reset graph")
        infoGBoxLayout.addWidget(resetGraphButton,3,0,1,8)
        resetGraphButton.clicked.connect(self.resetGraphButtonAction)

        # ---------------------------------------------------------------------
        #
        # ---------------------------------------------------------------------
        valIncControlGBox = QtGui.QGroupBox("Value increment adjustment")
        valIncControlGBoxLayout = QtGui.QGridLayout()
        valIncControlGBox.setLayout(valIncControlGBoxLayout)
        valIncControlGBox.setMaximumWidth(MINIMUM_WIDTH)
        valIncControlGBox.setMinimumWidth(MINIMUM_WIDTH)
        # ---------------------------------------------------------------------
        self.valIncControl_val0 = QtGui.QDoubleSpinBox()
        self.valIncControl_val0.setRange(0,100000000)
        self.valIncControl_val0.setSingleStep(1)
        self.valIncControl_val0.setValue(100)
        self.valIncControl_val0.setDecimals(0)
        self.valIncControl_val0.setKeyboardTracking(False)
        valIncControlGBoxLayout.addWidget(QtGui.QLabel("Val0 Increment: "),0,0)
        valIncControlGBoxLayout.addWidget(self.valIncControl_val0,0,1,1,6)
        # ---------------------------------------------------------------------
        self.valIncControl_val1 = QtGui.QDoubleSpinBox()
        self.valIncControl_val1.setRange(0,100000000)
        self.valIncControl_val1.setSingleStep(1)
        self.valIncControl_val1.setValue(200)
        self.valIncControl_val1.setDecimals(0)
        self.valIncControl_val1.setKeyboardTracking(False)
        valIncControlGBoxLayout.addWidget(QtGui.QLabel("Val1 Increment: "),1,0)
        valIncControlGBoxLayout.addWidget(self.valIncControl_val1,1,1,1,6)
        # ---------------------------------------------------------------------
        self.valIncControl_val2 = QtGui.QDoubleSpinBox()
        self.valIncControl_val2.setRange(0,100000000)
        self.valIncControl_val2.setSingleStep(1)
        self.valIncControl_val2.setValue(300)
        self.valIncControl_val2.setDecimals(0)
        self.valIncControl_val2.setKeyboardTracking(False)
        valIncControlGBoxLayout.addWidget(QtGui.QLabel("Val2 Increment: "),2,0)
        valIncControlGBoxLayout.addWidget(self.valIncControl_val2,2,1,1,6)
        # ---------------------------------------------------------------------
        self.valIncControl_val0.valueChanged.connect(self.updateValIncrements)
        self.valIncControl_val1.valueChanged.connect(self.updateValIncrements)
        self.valIncControl_val2.valueChanged.connect(self.updateValIncrements)

        # ---------------------------------------------------------------------
        #
        # ---------------------------------------------------------------------
        vbox_ui.addWidget(logoGBox)
        vbox_ui.addWidget(infoGBox)
        vbox_ui.addWidget(valIncControlGBox)
        vbox_ui.addStretch(1)

        # ---------------------------------------------------------------------
        #
        # ---------------------------------------------------------------------
        self.plot1 = pg.PlotWidget()
        self.plot2 = pg.PlotWidget()
        self.plot3 = pg.PlotWidget()
        self.plot4 = pg.PlotWidget()

        # ---------------------------------------------------------------------
        self.plot1.setLabel('bottom', 'time(sec)')
        self.plot2.setLabel('bottom', 'time(sec)')
        self.plot3.setLabel('bottom', 'time(sec)')
        self.plot4.setLabel('bottom', 'time(sec)')
        self.plot1.setLabel('left', '...')
        self.plot2.setLabel('left', '...')
        self.plot3.setLabel('left', '...')
        self.plot4.setLabel('left', '...')

        # ---------------------------------------------------------------------
        self.plot1.setTitle("Test Value 0")
        self.plot2.setTitle("Test Value 1")
        self.plot3.setTitle("Test Value 2")
        self.plot4.setTitle("Test Values Combined")

        # ---------------------------------------------------------------------
        #
        # ---------------------------------------------------------------------
        vbox_gr.addWidget(self.plot1, 0, 0)
        vbox_gr.addWidget(self.plot2, 0, 1)
        vbox_gr.addWidget(self.plot3, 1, 0)
        vbox_gr.addWidget(self.plot4, 1, 1)

        # ---------------------------------------------------------------------
        self.plot1_curve1 = pg.PlotCurveItem(pen=(1,1))
        self.plot1.addItem(self.plot1_curve1)

        # ---------------------------------------------------------------------
        self.plot2_curve1 = pg.PlotCurveItem(pen=(1,2))
        self.plot2.addItem(self.plot2_curve1)

        # ---------------------------------------------------------------------
        self.plot3_curve1 = pg.PlotCurveItem(pen=(1,3))
        self.plot3.addItem(self.plot3_curve1)

        # ---------------------------------------------------------------------
        self.plot4_curve1 = pg.PlotCurveItem(pen=(1,1))
        self.plot4_curve2 = pg.PlotCurveItem(pen=(1,2))
        self.plot4_curve3 = pg.PlotCurveItem(pen=(1,3))
        self.plot4.addItem(self.plot4_curve1)
        self.plot4.addItem(self.plot4_curve2)
        self.plot4.addItem(self.plot4_curve3)

        # ---------------------------------------------------------------------
        pg.setConfigOptions(antialias=True)

        # ---------------------------------------------------------------------
        #
        # ---------------------------------------------------------------------
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.PeriodicFunc)
        self.timer.start(33)

    # -------------------------------------------------------------------------
    def updateValIncrements(self):
        val0_inc = int(self.valIncControl_val0.value())
        val1_inc = int(self.valIncControl_val1.value())
        val2_inc = int(self.valIncControl_val2.value())

        arg = [val0_inc, val1_inc, val2_inc]

        hw.incrementValueSet(arg)

    # -------------------------------------------------------------------------
    def resetGraphButtonAction(self):
        hw.resetBuffers()

    # -------------------------------------------------------------------------
    def PeriodicFunc(self):
        [time, val0, val1, val2] = hw.getReadout()
        if(time != None):
            self.val0_label.setText(str(val0))
            self.val1_label.setText(str(val1))
            self.val2_label.setText(str(val2))

        [time_array, val0_array, val1_array, val2_array] = hw.getArrays()
        if(len(time_array) > 0):
            self.plot1_curve1.setData(x=time_array, y=val0_array)
            self.plot2_curve1.setData(x=time_array, y=val1_array)
            self.plot3_curve1.setData(x=time_array, y=val2_array)

            self.plot4_curve1.setData(x=time_array, y=val0_array)
            self.plot4_curve2.setData(x=time_array, y=val1_array)
            self.plot4_curve3.setData(x=time_array, y=val2_array)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    if(len(sys.argv) < 2):
        print("What is the port address?")

    else:
        print("Serial port name " + sys.argv[1])

        # Initalise hwrdware device
        hw = Hardware(sys.argv[1])

        # Initialise GUI
        app = QtGui.QApplication(sys.argv)
        window = UIClass()
        window.show()
        sys.exit(app.exec_())
