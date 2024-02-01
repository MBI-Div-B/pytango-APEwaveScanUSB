import ape_device
import numpy as np

class APEwaveScanUSBHandler(object):
    def __init__(self, host, port, name = "Ape device"):
        self.dev = ape_device.ape_device(host, port, name)
    def get_run(self):
        test = self.dev.query(":status:run?")
        return bool(int(test))
    def set_run(self,num):
        self.dev.send(":STATUS:RUN="+str(int(num)))
    def get_smooth(self):
        return int(self.dev.query(":STATUS:SMOOTH?"))
    def get_maxHold(self):
        return bool(int(self.dev.query(":STATUS:MAXHOLD?")))
    def get_avg(self):
        return int(self.dev.query(":STATUS:AVG?"))
    def get_peak(self, win=0):
        if win == 0:
            return float(self.dev.query(":SPECTRUM:PEAK?"))
        else:
            return float(self.dev.query(":SPECTRUM:"+str(win)+"PEAK?"))
    def get_FWHM(self, win=0):
        if win == 0:
            return float(self.dev.query(":SPECTRUM:FWHM?"))
        else:
            return float(self.dev.query(":SPECTRUM:"+str(win)+"FWHM?"))
    def get_center(self, win=0):
        if win == 0:
            return float(self.dev.query(":SPECTRUM:CENTER?"))
        else:
            return float(self.dev.query(":SPECTRUM:"+str(win)+"CENTER?"))
    def get_peakMax(self):
        return float(self.dev.query(":SPECTRUM:PEAK_MAX?"))
    def get_minWave(self):
        return float(self.dev.query(":measurement:wlrange:abs_min?"))
    def get_maxWave(self):
        return float(self.dev.query(":measurement:wlrange:abs_max?"))
    def get_minBoardWave(self,win=0):
        if win == 0:
            return float(self.dev.query(":measurement:wlrange:min?"))
        return float(self.dev.query(":measurement:peak"+str(win)+":min?"))
    def get_maxBoardWave(self,win=0):
        if win == 0:
            return float(self.dev.query(":measurement:wlrange:max?"))
        return float(self.dev.query(":measurement:peak"+str(win)+":max?"))
    def set_minBoardWave(self, num, win=0):
        if win == 0:
            self.dev.send(":measurement:wlrange:min "+str(num))
        self.dev.send(":measurement:peak"+str(win)+":min? " + str(num))
    def set_maxBoardWave(self, num, win=0):
        if win == 0:
            self.dev.send(":measurement:wlrange:max "+str(num))
        self.dev.send(":measurement:peak"+str(win)+":max? " + str(num))
    def get_Ewidth(self):
        return float(self.dev.query(":measurement:peak1:ewidth?"))
    def set_Ewidth(self,num):
        self.dev.send(":measurement:peak1:ewidth "+str(num))

    def get_fit(self):
        if bool(int(self.dev.query(':measurement:fit:enabled?'))):
            return {"GAUSS":1, "LORENTZ":2, "SECH2y":3}[self.dev.query(':measurement:fit:type?')]
        return 0
    def set_fit(self,num):
        if num == 0:
            self.dev.send(":measurement:fit:enabled=0")
        else:
            self.dev.send(":measurement:fit:enabled=1")
            self.dev.send(":measurement:fit:type "+str(num))

    def get_Data(self):
        acf_binary_data = bytes(self.dev.query(":SPECTRUM:DATA?",block=True))
        acf = np.fromstring(acf_binary_data, dtype=np.float64)
        acf = acf.reshape(int(acf.shape[0]/2),2)
        return acf.T

    def get_fitData(self):
        acf_binary_data = bytes(self.dev.query(":MEASUREMent:FIT:DATA?",block=True))
        acf = np.fromstring(acf_binary_data, dtype=np.float64)
        acf = acf.reshape(int(acf.shape[0]/2),2)
        return acf.T
    
    def get_fourLim(self):
        print(self.dev.query(':measurement:fourier_limit:enabled?'))
        return bool(int(self.dev.query(':measurement:fourier_limit:enabled?')))
    
    def set_fourLim(self,num):
        self.dev.send(':measurement:fourier_limit:enabled='+str(int(num)))
    
    def get_gain(self):
        print(self.dev.query(":MEASUREMENT:GAIN?"))
        return {'1':0,'2':1,'5':2,'10':3}[self.dev.query(":MEASUREMENT:GAIN?")]
    def set_gain(self,num):
        self.dev.send(":MEASUREMENT:GAIN "+{'0':"1",'1':"2",'2':"5",'3':"10"}[str(num)])