# gui.py: contains PyQt4 classes for Nostradamus Tracker
# Written for UCLA's ELFIN mission <elfin.igpp.ucla.edu>
# By Micah Cliffe (KK6SLK) <micah.cliffe@ucla.edu>

import sys
from PyQt4 import QtGui, QtCore

RES = "res/"

###############################################################################
class SimpleTracker(QtGui.QMainWindow):

    def __init__(self, predictor):
        super(SimpleTracker, self).__init__()
        self.predictor = predictor
        self.setObjectName("SimpleTracker")
        self.resize(238, 178)
        '''
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(RES + "icon.png"), QtGui.QIcon.Normal, 
                       QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        '''
        w = self.centralwidget = QtGui.QWidget()
        self.label_az = QtGui.QLabel(self.centralwidget)
        self.label_az.setGeometry(QtCore.QRect(30, 70, 71, 21))
        self.label_az.setObjectName("label_az")
        self.label_el = QtGui.QLabel(self.centralwidget)
        self.label_el.setGeometry(QtCore.QRect(20, 100, 81, 21))
        self.label_el.setObjectName("label_el")
        self.label_station = QtGui.QLabel(self.centralwidget)
        self.label_station.setGeometry(QtCore.QRect(0, 10, 101, 21))
        self.label_station.setObjectName("label_station")
        self.label_satellite = QtGui.QLabel(self.centralwidget)
        self.label_satellite.setGeometry(QtCore.QRect(30, 40, 71, 21))
        self.label_satellite.setObjectName("label_satellite")
        self.refreshButton = QtGui.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(100, 130, 101, 31))
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.clicked.connect(self.onRefresh)
        self.ESN_val = QtGui.QLabel(self.centralwidget)
        self.ESN_val.setGeometry(QtCore.QRect(100, 10, 131, 21))
        self.ESN_val.setObjectName("ESN_val")
        self.sat_val = QtGui.QLabel(self.centralwidget)
        self.sat_val.setGeometry(QtCore.QRect(100, 40, 131, 21))
        self.sat_val.setObjectName("sat_val")
        self.az_val = QtGui.QLabel(self.centralwidget)
        self.az_val.setGeometry(QtCore.QRect(100, 70, 131, 21))
        self.az_val.setObjectName("az_val")
        self.el_val = QtGui.QLabel(self.centralwidget)
        self.el_val.setGeometry(QtCore.QRect(100, 100, 131, 21))
        self.el_val.setObjectName("el_val")
        self.setCentralWidget(self.centralwidget)

        self.setWindowTitle("Simple Tracking")
        self.label_az.setText(" Azimuth:")
        self.label_el.setText("  Elevation:")
        self.label_station.setText(" Earth Station:")
        self.label_satellite.setText(" Satellite:")
        self.refreshButton.setText("Refresh")
        self.ESN_val.setText("Unknown")
        self.sat_val.setText("Unknown")
        self.az_val.setText("Unknown")
        self.el_val.setText("Unknown")
        self.show()

    def onRefresh(self):
        p       = self.predictor
        sat     = p.getSatellites()[0]
        station = p.getStation()
        pos     = p.position(sat)
        self.ESN_val.setText(station)
        self.sat_val.setText(sat)
        self.az_val.setText(str(pos[0]))
        self.el_val.setText(str(pos[1]))

################################################################################
def main():
    app = QtGui.QApplication(sys.argv)
    ex  = SimpleTracker()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()  
