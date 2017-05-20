# gui.py: contains core functionality for Nostradamus Tracker
# Written for UCLA's ELFIN mission <elfin.igpp.ucla.edu>
# By Micah Cliffe (KK6SLK) <micah.cliffe@ucla.edu>

import datetime
import urllib
import ephem
import numpy as np

CUBESATS = "http://www.celestrak.com/NORAD/elements/cubesat.txt"

################################################################################
class Station(ephem.Observer):
    def __init__(self, name=None, location=(0,0), elevation=0, callsign=None):
        super(Station, self).__init__()
        self.name = name
        ''' Possible issue in not setting lat and long ''' 
        if (name.upper() == "KNUDSEN"):
            self.lat       = np.deg2rad(34.07045)
            self.long      = np.deg2rad(-118.441114)
            self.elevation = 150 # meters
            self.callsign  = "W6YRA"
        else:
            self.lat       = np.deg2rad(location[0])
            self.long      = np.deg2rad(location[1])
            self.elevation = elevation
            self.callsign  = callsign

################################################################################
# TODO: inherit from ephem Body!!!!!
class Satellite(object):
    def __init__(self, body, name="FIREBIRD 4", owner=None, uplink=None, 
                 downlink=None, mode=None, callsign=None):
        ''' @param body
                a PyEphem body
        '''
        self.body = body
        self.name = body.name
        #self.name = name = name.upper()
        if (name == "FIREBIRD 4"): #or name == "FIREBIRD"):
            #if (name == "FIREBIRD"):
            #    self.name = "FIREBIRD 4"
            self.owner    = "Montana State University"
            self.uplink   = "" 
            self.downlink = "437.219 MHz" 
            self.mode     = "19200bps FSK"
            self.callsign = "K7MSU"
        elif (name == "ELFIN" or name == "UCLA"):
            if (name == "UCLA"):
                self.name = "ELFIN"
            self.owner    = "University of California, Los Angeles"
            self.uplink   = "144.4 MHz" 
            self.downlink = "437.45 MHz" 
            self.mode     = "9k6 uplink, 19k2 downlink"
            self.callsign = "W6YRA"
        else:
            self.owner    = owner
            self.uplink   = uplink
            self.downlink = downlink
            self.mode     = mode
            self.callsign = callsign

    def getPosition(self, observer):
        body = self.body
        body.compute(observer)
        return (body.az, body.alt)

################################################################################
class Predictor(object):
    def __init__(self, knudsen=True):
        ''' @param knudsen
                if the Earth Station is Knudsen, use Knudsen
                else, manually call setStation immediately after Predictor 
                creation
        '''
        self._station = None
        if (knudsen):
            self._station = station = Station("KNUDSEN")
        self._sats = []
        # TODO: call self.updateTLEs() automatically upon creating maybe

    ### Station Details ###

    def setStation(self, name=None, location=(0,0), elevation=0, callsign=None):
        self._station = Station(name, location, elevation, callsign)

    def getStation(self):
        if hasattr(self._station, 'name'):
            return self._station.name 
        return None 

    ### Satellite Details ###

    def addSatellite(self, name, owner=None, uplink=None, 
                     downlink=None, mode=None, callsign=None):
        if (name.upper() == "FIREBIRD"):
            name = "FIREBIRD 4"
        for s in self._sats:
            if (name == sat.name):
                print("Satellite already exists.")
                return False
        body = self.loadTLE(name)
        if not body:
            print("TLE not found for " + name)
            return False
        sat = Satellite(body, name, owner, uplink, downlink, mode, callsign)
        self._sats.append(sat)
        return True

    def removeSatellite(self, name):
        for s in self._sats:
            if (s.name == name):
                self._sats.remove(s)
                return True
        return False

    def getSatellite(self, name):
        for s in self._sats:
            if s.name == name:
                return s
        return None

    def getSatellites(self):
        return [s.name for s in self._sats]

    ### TLE Details ###

    def updateTLEs(self, url=CUBESATS):
        try:
            urllib.urlretrieve(url, "tle.txt")
        except Exception as e:
            print(e)
            print("Failed to update TLEs.")
            return False
        return True

    # Not used probably
    def loadTLEs(self, filename="tle.txt"):
        with open(filename, 'r') as f:
            sats = []
            l1   = f.readline()
            while l1:
                l2  = f.readline()
                l3  = f.readline()
                sat = ephem.readtle(l1, l2, l3)
                sats.append(sat)
                print sat.name
                l1 = f.readline()
        print("%i satellites loaded."%len(sats))
        return sats

    def loadTLE(self, satName, filename="tle.txt"):
        sat = None
        with open(filename, 'r') as f:
            l1  = f.readline()
            while l1:
                if satName in l1:
                    l2  = f.readline()
                    l3  = f.readline()
                    sat = ephem.readtle(l1, l2, l3)
                    break
                f.readline()
                f.readline()
                l1 = f.readline()
        return sat

    ### Performance Functions ###

    def position(self, satName, date=None):
        # TODO: date = now however I do that    
        if not date:
            date = datetime.datetime.now()
        self._station.date = date
        sat = None
        for s in self._sats:
            if (s.name == satName):
                sat = s
                break
        if sat:
            return sat.getPosition(self._station)
        return None

#TODO: what happens when TLE file doesn't exist, when can't update, when
#      can't read?
################################################################################
if __name__ == "__main__":
    n = Predictor()
    n.updateTLEs()
    print n.getStation()
    print n.addSatellite("firebird")
    print n.getSatellites()
    print n.removeSatellite("FIREBIRD 4")
    print n.getSatellites()
    n.addSatellite("firebird")
    pos = n.position("FIREBIRD 4")
    print pos
