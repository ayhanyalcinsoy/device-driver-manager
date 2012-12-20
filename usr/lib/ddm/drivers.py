#!/usr/bin/env python

import threading
from nvidia import Nvidia
from ati import ATI
from intel import Intel
from via import Via
from broadcom import Broadcom
from pae import PAE

hwCodes = ['nvidia', 'ati', 'intel', 'via', 'broadcom', 'pae']


# Class to check for supported drivers
class DriverGet(threading.Thread):
    def __init__(self, distribution, loggerObject, hwCode, queue):
        threading.Thread.__init__(self)
        self.log = loggerObject
        self.log.write('Initialize DriverGet', 'drivers.DriverGet', 'debug')
        self.distribution = distribution
        self.hwCode = hwCode
        self.queue = queue

    # This will only check for Nvidia, ATI, Broadcom and PAE
    def run(self):
        hwList = []

        if self.hwCode == hwCodes[0]:
            nv = Nvidia(self.distribution, self.log)
            hwList = nv.getNvidia()
        elif self.hwCode == hwCodes[1]:
            ati = ATI(self.distribution, self.log)
            hwList = ati.getATI()
        elif self.hwCode == hwCodes[2]:
            intel = Intel(self.distribution, self.log)
            hwList = intel.getIntel()
        elif self.hwCode == hwCodes[3]:
            via = Via(self.distribution, self.log)
            hwList = via.getVia()
        elif self.hwCode == hwCodes[4]:
            bc = Broadcom(self.distribution, self.log)
            hwList = bc.getBroadcom()
        elif self.hwCode == hwCodes[5]:
            pae = PAE(self.distribution, self.log)
            hwList = pae.getPae()

        self.queue.put(hwList)
        self.queue.task_done()


# Driver install class needs threading
class DriverInstall(threading.Thread):
    def __init__(self, distribution, loggerObject, hwCode, driver=''):
        threading.Thread.__init__(self)
        self.log = loggerObject
        self.hwCode = hwCode
        self.driver = driver
        self.log.write('Initialize DriverInstall', 'drivers.DriverInstall', 'debug')
        self.distribution = distribution

    # Install hardware drivers for given hardware code and driver
    def run(self):
        if self.hwCode == hwCodes[0]:
            nv = Nvidia(self.distribution, self.log)
            nv.installNvidia(self.driver)
        elif self.hwCode == hwCodes[1]:
            ati = ATI(self.distribution, self.log)
            ati.installATI(self.driver)
        elif self.hwCode == hwCodes[2]:
            intel = Intel(self.distribution, self.log)
            intel.installIntel(self.driver)
        elif self.hwCode == hwCodes[3]:
            via = Via(self.distribution, self.log)
            via.installVia(self.driver)
        elif self.hwCode == hwCodes[4]:
            bc = Broadcom(self.distribution, self.log)
            bc.installBroadcom(self.driver)
        elif self.hwCode == hwCodes[5]:
            pae = PAE(self.distribution, self.log)
            pae.installPAE()


# Driver install class needs threading
class DriverRemove(threading.Thread):
    def __init__(self, distribution, loggerObject, hwCode, driver=''):
        threading.Thread.__init__(self)
        self.log = loggerObject
        self.hwCode = hwCode
        self.driver = driver
        self.log.write('Initialize DriverRemove', 'drivers.DriverRemove', 'debug')
        self.distribution = distribution

    # Install hardware drivers for given hardware codes (hwCodes)
    def run(self):
        # Instantiate driver classes
        if self.hwCode == hwCodes[0]:
            nv = Nvidia(self.distribution, self.log)
            nv.removeNvidia(self.driver)
        elif self.hwCode == hwCodes[1]:
            ati = ATI(self.distribution, self.log)
            ati.removeATI(self.driver)
        elif self.hwCode == hwCodes[2]:
            intel = Intel(self.distribution, self.log)
            intel.removeIntel(self.driver)
        elif self.hwCode == hwCodes[3]:
            via = Via(self.distribution, self.log)
            via.removeVia(self.driver)
        elif self.hwCode == hwCodes[4]:
            bc = Broadcom(self.distribution, self.log)
            bc.removeBroadcom(self.driver)
        elif self.hwCode == hwCodes[5]:
            pae = PAE(self.distribution, self.log)
            pae.removePAE()