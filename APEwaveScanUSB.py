import APEwaveScanUSBHandler
from tango import AttrWriteType, DevState, AttrWriteType, DispLevel, DebugIt
from tango.server import Device, attribute, command, device_property
from enum import IntEnum, Flag
import numpy as np

class fitEnum(IntEnum):
    OFF = 0
    GAUSSIAN = 1
    SECH2 = 2
    LORENTZ = 3



class APEwaveScanUSB(Device):
    # device properties
    Host = device_property(
        dtype=str,
    )
    Port = device_property(
        dtype=int,
    )

    run = attribute(
        label= 'Set measurement status',
        dtype= "DevBoolean",
        access= AttrWriteType.READ_WRITE
    )
    smooth = attribute(
        label= 'Smoothing function status',
        dtype= "DevBoolean",
        access= AttrWriteType.READ
    )
    maxHold = attribute(
        label= 'Maxhold function status',
        dtype= "DevBoolean",
        access= AttrWriteType.READ_WRITE
    )
    avg = attribute(
        label= 'Number of Measurements used for averaging',
        dtype= int,
        access= AttrWriteType.READ
    )
    peak = attribute(
        label= 'peak wavelength',
        dtype= "DevDouble",
        access= AttrWriteType.READ
    )
    FWHM = attribute(
        label="FWHM",
        dtype=float,
        access=AttrWriteType.READ
    )
    center = attribute(
        label = 'center wavelenth',
        dtype = float,
        access = AttrWriteType.READ
    )
    
    peakMax = attribute(
        label = 'maxiuum intensity value',
        dtype = 'DevDouble',
        access = AttrWriteType.READ
    )
    peak1 = attribute(
        label= 'peak wavelength for window 1',
        dtype= "DevDouble   ",
        access= AttrWriteType.READ
    )
    FWHM1 = attribute(
        label="FWHM for window 1",
        dtype=float,
        access=AttrWriteType.READ
    )
    center1 = attribute(
        label = 'center wavelenth for window 1',
        dtype = float,
        access = AttrWriteType.READ
    )
    peak2 = attribute(
        label= 'peak wavelength for window 2',
        dtype= "DevDouble   ",
        access= AttrWriteType.READ
    )
    FWHM2 = attribute(
        label="FWHM for window 2",
        dtype=float,
        access=AttrWriteType.READ
    )
    center2 = attribute(
        label = 'center wavelenth for window 2',
        dtype = float,
        access = AttrWriteType.READ
    )
    maxWave = attribute(
        label = 'maximum wavelength measureable',
        dtype = 'DevDouble',
        access = AttrWriteType.READ
    )
    minWave = attribute(
        label = 'minimum wavelength measureable',
        dtype = 'DevDouble',
        access = AttrWriteType.READ
    )
    maxBoardWave = attribute(
        label = 'set upper wavelength boarder of measurement window',
        dtype = 'DevDouble',
        access = AttrWriteType.READ_WRITE
    )
    minBoardWave = attribute(
        label = 'set upper wavelength boarder of measurement window',
        dtype = 'DevDouble',
        access = AttrWriteType.READ_WRITE
    )
    maxBoardWave1 = attribute(
        label = 'set upper wavelength boarder of peak window 1',
        dtype = 'DevDouble',
        access = AttrWriteType.READ_WRITE
    )
    minBoardWave1 = attribute(
        label = 'set upper wavelength boarder of peak window 1',
        dtype = 'DevDouble',
        access = AttrWriteType.READ_WRITE
    )
    Ewidth1 = attribute(
        lable = 'Set expected spectral width for peak window 1 measurements',
        dtype = 'DevDouble',
        access = AttrWriteType.READ_WRITE
    )
    maxBoardWave2 = attribute(
        label = 'set upper wavelength boarder of peak window 2',
        dtype = 'DevDouble',
        access = AttrWriteType.READ_WRITE
    )
    minBoardWave2 = attribute(
        label = 'set upper wavelength boarder of peak window 2',
        dtype = 'DevDouble',
        access = AttrWriteType.READ_WRITE
    )
    fit = attribute(
        label = ' type of function to fit through the measured data',
        dtype = fitEnum,
        access = AttrWriteType.READ_WRITE
    )
    
    fitData = attribute(
        label = 'fitted data',
        dtype = ((float,),),
        max_dim_x=1024,
        max_dim_y=1024,
        access = AttrWriteType.READ
    )

    Data = attribute(
        label = 'measured Data',
        dtype = ((float,),),
        max_dim_x=1024,
        max_dim_y=1024,
        access = AttrWriteType.READ
    )

    fourLim = attribute(
        label = 'Set status of fourier limit (peak 1) calculation',
        dtype = bool,
        access = AttrWriteType.READ_WRITE
    )
    

    def init_device(self):
        Device.init_device(self)
        self.set_state(DevState.INIT)
        self.wav = APEwaveScanUSBHandler.APEwaveScanUSBHandler(self.Host, self.Port)
        self.set_state(DevState.ON)
        self.debug_stream("init done")
    

    def read_run(self):
        return self.wav.get_run()

    def write_run(self,num):
        self.wav.set_run(num)
        
    def read_smooth(self):
        return self.wav.get_smooth()

    def read_maxHold(self):
        return self.wav.get_maxHold()

    def read_avg(self):
        return self.wav.avg()
    
    def read_peak(self):
        return self.wav.get_peak()

    def read_FWHM(self):
        return self.wav.get_FWHM()

    def read_center(self):
        return self.wav.get_center()

    def read_peakMax(self):
        return self.wav.get_peakMax()

    def read_peak1(self):
        return self.wav.get_peak()
        
    def read_FWHM1(self):
        return self.wav.get_FWHM()

    def read_center1(self):
        return self.wav.get_center()

    def read_peak2(self):
        return self.wav.get_peak()
        
    def read_FWHM2(self):
        return self.wav.get_FWHM()

    def read_center2(self):

        return self.wav.get_center()

    def read_maxWave(self):
        return self.wav.get_maxWave()
    def read_minWave(self):
        return self.wav.get_minWave()
    def write_maxBoardWave(self,num):
        self.wav.set_maxBoardWave(num)
    def read_maxBoardWave(self):
        return self.wav.get_maxBoardWave()
    def write_minBoardWave(self,num):
        self.wav.set_minBoardWave(num)
    def read_minBoardWave(self):
        return self.wav.get_minBoardWave()
    def write_maxBoardWave1(self,num,win=1):
        self.wav.set_maxBoardWave(num)
    def read_maxBoardWave1(self,win=1):
        return self.wav.get_maxBoardWave()
    def write_minBoardWave1(self,num,win=1):
        self.wav.set_minBoardWave(num)
    def read_minBoardWave1(self,win=1):
        return self.wav.get_minBoardWave()
    def write_maxBoardWave1(self,num,win=2):
        self.wav.set_maxBoardWave(num)
    def read_maxBoardWave1(self,win=2):
        return self.wav.get_maxBoardWave()
    def write_minBoardWave1(self,num,win=2):
        self.wav.set_minBoardWave(num)
    def read_minBoardWave1(self,win=2):
        return self.wav.get_minBoardWave()
    def read_Ewidth1(self):
        return self.wav.get_Ewidth()
    def write_Ewidth1(self,num):
        self.wav.set_Ewidth(num)
    def read_fit(self):
        return self.wav.get_fit()
    def write_fit(self,num):
        self.wav.set_fit(num)
    def read_fourLim(self):
        return self.wav.get_fourLim()
    def write_fourLim(self,num):
        self.wav.set_fourLim(num)
    def read_Data(self):
        return self.wav.get_Data()
    def read_fitData(self):
        return self.wav.get_fitData()


    
if __name__ == "__main__":
    APEwaveScanUSB.run_server()

