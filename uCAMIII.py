
import serial, uCAMIII_codes
import time
import re
from binascii import hexlify, unhexlify
from struct import pack, unpack
import codecs
from PIL import Image
import io
import numpy as np
class UCam():
    
    def __init__(self):
        self.ser = serial.Serial(port = "COM4", baudrate=115200, timeout=2)
        self.synced=False
        print("Serial port set")
        
    def init(self ,picType = 'jpeg', rawRes='80x60', jpegRes = '160x128'):
        if picType is 'jpeg':
            picCmd = uCAMIII_codes.uCamIII_COMP_JPEG
        elif picType is 'raw':
            picCmd = uCAMIII_codes.uCamIII_RAW_8BIT
        elif picType is 'raw16':
            picCmd = uCAMIII_codes.uCamIII_RAW_16BIT_RGB565
        elif picType is 'rawCy':
            picCmd = uCAMIII_codes.uCamIII_RAW_16BIT_CRYCBY
        else:
            print('Please enter correct picture type');
            sys.exit(1)

        if rawRes is '80x60':
            rawRes_cmd = uCAMIII_codes.uCamIII_80x60
        elif rawRes is '160x120':
            rawRes_cmd = uCAMIII_codes.uCamIII_160x120
        elif rawRes is '128x128':
            rawRes_cmd = uCAMIII_codes.uCamIII_128x128
        elif rawRes is '128x96':
            rawRes_cmd = uCAMIII_codes.uCamIII_128x96
        else:
            print('Please enter correct raw resolution')
            sys.exit(1)
        if jpegRes is '160x128':
            jpegRes_cmd = uCAMIII_codes.uCamIII_160x128
        elif jpegRes is '320x240':
            jpegRes_cmd = uCAMIII_codes.uCamIII_320x240
        elif jpegRes is '640x480':
            jpegRes_cmd = uCAMIII_codes.uCamIII_640x480

        init_cmd = uCAMIII_codes.init_cmd(picCmd, rawRes_cmd, jpegRes_cmd)
        self.send_cmd(init_cmd)
        read = self.response(6)

        assert self.equals(uCAMIII_codes.ack_cmd(uCAMIII_codes.uCamIII_CMD_INIT, 'FF'), read)
    
    def sync(self):
        tries = 60
        
        while tries > 0:
            if self._sync():
                return True
            tries -= 1
        return False

    def _sync(self):
        time.sleep(.05)
        self.send_cmd(uCAMIII_codes.sync())
        read = self.ser.read(6)
        print(read)
        if(self.equals(uCAMIII_codes.ack_cmd(uCAMIII_codes.uCamIII_CMD_SYNC, '00'), read)):
            if(self.equals(uCAMIII_codes.sync(), self.ser.read(6))):
                self.send_cmd(uCAMIII_codes.ack_cmd(uCAMIII_codes.uCamIII_CMD_SYNC, 'FF'))
                return True
        return False
    
    def snapshot(self, snapType='jpeg'):
        if snapType is 'jpeg':
            snap_cmd = uCAMIII_codes.uCamIII_SNAP_JPEG
        elif snapType is 'raw':
            snap_cmd = uCAMIII_codes.uCamIII_SNAP_RAW
        else:
            print('Please enter correct snapshot type')
            sys.exit(1)
            
        self.send_cmd(uCAMIII_codes.snapshot(snap_cmd, '00', '00'))
      
        assert self.equals(uCAMIII_codes.ack_cmd(uCAMIII_codes.uCamIII_CMD_SNAPSHOT, 'ff'), self.response(6))

    def set_pkg_size():
        self.send_cmd(uCAMIII_codes.set_pkg_size('02', '00'))
        assert self.equals(uCAMIII_codes.ack_cmd(uCAMIII_codes.uCamIII_CMD_SET_PACKSIZE, 'FF'), self.response(6))

    def get_picture(self, picType='jpeg'):

        if picType is 'jpeg':
            picType_cmd = uCAMIII_codes.uCamIII_TYPE_JPEG
        elif picType is 'raw':
            picType_cmd = uCAMIII_codes.uCamIII_TYPE_RAW
        elif picType is 'snap':
            picType_cmd = uCAMIII_codes.uCamIII_TYPE_SNAPSHOT
        else:
            print('Please enter correct picture type')
            sys.exit(1)

        self.send_cmd(uCAMIII_codes.get_pic(picType_cmd))
        assert self.equals(uCAMIII_codes, self.response(6))

        data = self.response(6)

        assert self.equals(uCAMIII_codes.data(picType_cmd, '..' ,'..', '..'), data)

        img_size = unpack('<I', (data[-3:] + b'\x00'))[0]

        self.send_cmd(uCAMIII_codes.ack_cmd('00', '00'))

        return img_size

    def write_pic(self, img_size):

        num_pkgs = 1

        read = self.response(4800)
        print(hexlify(read))
        gray = np.array(read).reshape(60,80)
        img = Image.fromarray(gray)
        self.send_cmd(uCAMIII_codes.ack_cmd(uCAMIII_codes.uCamIII_CMD_DATA, '00', '01', '00'))
        return img

    def send_cmd(self, cmd_str):
        return self.ser.write(bytearray(unhexlify(cmd_str)))

    def response(self, bytes):
        bytearr = bytearray(bytes)
        cur = 0
        while cur < bytes:
            read=self.ser.read(1)
            if len(read) == 1:
                bytearr[cur] = read[0]
                cur+=1
        return bytearr
   
    def equals(self, pattern, packet):
        packet_str = hexlify(packet)
        return re.match(pattern, packet_str.decode()) is not None