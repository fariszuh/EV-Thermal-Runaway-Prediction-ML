# -----------------------------------------------------------------------------
#
#
# -----------------------------------------------------------------------------
import sys
import time
import serial
import struct
import threading
import numpy as np
from datetime import datetime

# -----------------------------------------------------------------------------
tmpbuf = [0] * 64
BAUD_RATE = 115200
THREAD_WAIT_SEC = 0.01

#------------------------------------------------------------------------------
def print_hex(buff):
    print(' '.join('%02x'%i for i in buff))

#------------------------------------------------------------------------------
def make32b(buff, offset):
    rv  = buff[offset + 0]
    rv += buff[offset + 1] << 8
    rv += buff[offset + 2] << 16
    rv += buff[offset + 3] << 24
    return rv

#------------------------------------------------------------------------------
def put32b(buff, offset, val):
    buff[offset + 0] = (val & 0x000000FF) >> 0
    buff[offset + 1] = (val & 0x0000FF00) >> 8
    buff[offset + 2] = (val & 0x00FF0000) >> 16
    buff[offset + 3] = (val & 0xFF000000) >> 24

# -----------------------------------------------------------------------------
class Hardware():

    # -------------------------------------------------------------------------
    def __init__(self, portAddress):
        self.readout = [0, 0, 0, 0]
        self.time_array = []
        self.val0_array = []
        self.val1_array = []
        self.val2_array = []
        try:
            self.start_time = datetime.now()
            self.sp = serial.Serial(portAddress, 115200, timeout=0.1)
            self.sp.flush()
            self.bufferLock = threading.Lock()
            thread = threading.Thread(target=self.updateThread, args=())
            thread.daemon = True
            thread.start()
        except ValueError as e:
            print("Serial port error ...")
            return None

    # -------------------------------------------------------------------------
    def sendUpdateRequest(self):
        tmpbuf[0] = 2
        tmpbuf[1] = 1
        self.sp.write(tmpbuf[0:2])

    # -------------------------------------------------------------------------
    def incrementValueSet(self, arg):
        [val0_inc, val1_inc, val2_inc] = arg
        self.bufferLock.acquire()
        tmpbuf[0] = 14
        tmpbuf[1] = 2
        put32b(tmpbuf, 2, val0_inc)
        put32b(tmpbuf, 6, val1_inc)
        put32b(tmpbuf, 10, val2_inc)
        self.sp.write(tmpbuf[0:14])
        self.bufferLock.release()

    # -------------------------------------------------------------------------
    def resetBuffers(self):
        self.bufferLock.acquire()
        self.time_array = []
        self.val0_array = []
        self.val1_array = []
        self.val2_array = []
        self.bufferLock.release()

    # -------------------------------------------------------------------------
    def updateThread(self):

        # Wait for bootup
        time.sleep(5)

        # Run forever ...
        while True:

            # lock
            self.bufferLock.acquire()

            # ask
            self.sendUpdateRequest()

            # read
            rbuf = self.sp.read(12)

            # check
            if(len(rbuf) == 12):

                val0 = make32b(rbuf, 0)
                val1 = make32b(rbuf, 4)
                val2 = make32b(rbuf, 8)

                # calculate time since begining
                time_now = datetime.now()
                timeCounter = (time_now - self.start_time).total_seconds()

                # put into array for later reading
                self.readout = [timeCounter, val0, val1, val2]

                # append to graph buffers
                self.time_array = np.append(self.time_array, timeCounter)
                self.val0_array = np.append(self.val0_array, val0)
                self.val1_array = np.append(self.val1_array, val1)
                self.val2_array = np.append(self.val2_array, val2)

            # unlock
            self.bufferLock.release()

            # wait
            time.sleep(THREAD_WAIT_SEC)

    # -------------------------------------------------------------------------
    def getReadout(self):
        self.bufferLock.acquire()
        tmp = self.readout
        self.bufferLock.release()
        return tmp

    # -------------------------------------------------------------------------
    def getArrays(self):
        self.bufferLock.acquire()
        tmp = [self.time_array, self.val0_array, self.val1_array, self.val2_array]
        self.bufferLock.release()
        return tmp

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    if(len(sys.argv) < 2):
        print("What is serial port?")
        sys.exit(0)

    print("Serial port: " + sys.argv[1])

    hw = Hardware(sys.argv[1])

    while True:
        time.sleep(0.1)
        print(hw.getReadout())
