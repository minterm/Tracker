#!/usr/bin/python
# -*- coding: utf-8 -*-

# main.py: run the Nostradamus Tracker
# Written for UCLA's ELFIN mission <elfin.igpp.ucla.edu>
# By Micah Cliffe (KK6SLK) <micah.cliffe@ucla.edu>

import sys
from PyQt4       import QtGui
from gui         import SimpleTracker
from nostradamus import Predictor

################################################################################
def main():
    p = Predictor()
    p.updateTLEs()
    p.addSatellite("FIREBIRD 4")

    app = QtGui.QApplication(sys.argv)
    ex  = SimpleTracker(p)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()  
