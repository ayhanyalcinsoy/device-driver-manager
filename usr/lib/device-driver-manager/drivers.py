#!/usr/bin/env python

import threading
import functions
from mirror import Mirror
from nvidia import Nvidia
from ati import ATI
from broadcom import Broadcom
from pae import PAE

packageStatus = ['installed', 'notinstalled', 'uninstallable']
hwCodes = ['nvidia', 'ati', 'broadcom', 'pae', 'mirror']


# Class to check for supported drivers
class DriverCheck():
    def __init__(self, loggerObject):
        self.log = loggerObject
        self.log.write('Initialize DriverCheck', 'drivers.DriverCheck', 'debug')
        self.distribution = functions.getDistribution()

    # This will only check for Nvidia, ATI, Broadcom and PAE
    def run(self):
        hwList = []

        #mir = Mirror(self.distribution, self.log)
        nv = Nvidia(self.distribution, self.log)
        ati = ATI(self.distribution, self.log)
        bc = Broadcom(self.distribution, self.log)
        pae = PAE(self.distribution, self.log)

        # Collect supported hardware
        #mirror = mir.getFastestMirror()
        hwNvidia = nv.getNvidia()
        hwATI = ati.getATI()
        hwBroadcom = bc.getBroadcom()
        hwPae = pae.getPae()

        # Combine all found hardware in a single list
        #for line in mirror:
        #    hwList.append(line)
        for line in hwPae:
            hwList.append(line)
        for line in hwNvidia:
            hwList.append(line)
        for line in hwATI:
            hwList.append(line)
        for line in hwBroadcom:
            hwList.append(line)

        return hwList


# Driver install class needs threading
class DriverInstall(threading.Thread):
    def __init__(self, hwCodesWithStatusList, loggerObject):
        threading.Thread.__init__(self)
        self.log = loggerObject
        self.log.write('Initialize DriverInstall', 'drivers.DriverInstall', 'debug')
        self.hwCodesWithStatusList = hwCodesWithStatusList
        self.distribution = functions.getDistribution()

    # Install hardware drivers for given hardware codes (hwCodes)
    def run(self):
        # Instantiate driver classes
        mir = Mirror(self.distribution, self.log)
        nv = Nvidia(self.distribution, self.log)
        ati = ATI(self.distribution, self.log)
        bc = Broadcom(self.distribution, self.log)
        pae = PAE(self.distribution, self.log)

        # First check for mirror
        for code in self.hwCodesWithStatusList:
            if code[0] == hwCodes[4]:
                if code[1] != packageStatus[2]:
                    mir.installMirror()

        # Now install the hardware drivers
        for code in self.hwCodesWithStatusList:
            # First check for mirror
            if code[0] != hwCodes[4]:
                if code[0] == hwCodes[0]:
                    if code[1] != packageStatus[2]:
                        nv.installNvidia()
                elif code[0] == hwCodes[1]:
                    if code[1] != packageStatus[2]:
                        ati.installATI()
                elif code[0] == hwCodes[2]:
                    if code[1] != packageStatus[2]:
                        bc.installBroadcom()
                elif code[0] == hwCodes[3]:
                    if code[1] != packageStatus[2]:
                        pae.installPAE()


# Driver install class needs threading
class DriverRemove(threading.Thread):
    def __init__(self, hwCodesWithStatusList, loggerObject):
        threading.Thread.__init__(self)
        self.log = loggerObject
        self.log.write('Initialize DriverRemove', 'drivers.DriverRemove', 'debug')
        self.hwCodesWithStatusList = hwCodesWithStatusList
        self.distribution = functions.getDistribution()

    # Install hardware drivers for given hardware codes (hwCodes)
    def run(self):
        # Instantiate driver classes
        mir = Mirror(self.distribution, self.log)
        nv = Nvidia(self.distribution, self.log)
        ati = ATI(self.distribution, self.log)
        bc = Broadcom(self.distribution, self.log)
        pae = PAE(self.distribution, self.log)

        for code in self.hwCodesWithStatusList:
            if code[0] == hwCodes[0]:
                if code[1] == packageStatus[0]:
                    nv.removeNvidia()
            elif code[0] == hwCodes[1]:
                if code[1] == packageStatus[0]:
                    ati.removeATI()
            elif code[0] == hwCodes[2]:
                if code[1] == packageStatus[0]:
                    bc.removeBroadcom()
            elif code[0] == hwCodes[3]:
                if code[1] == packageStatus[0]:
                    pae.removePAE()
            if code[0] == hwCodes[4]:
                if code[1] != packageStatus[2]:
                    mir.removeMirror()
