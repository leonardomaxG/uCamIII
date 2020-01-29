

ID                          ='aa'
uCamIII_CMD_INIT			= '01'
uCamIII_CMD_GET_PICTURE		= '04'
uCamIII_CMD_SNAPSHOT		= '05'
uCamIII_CMD_SET_PACKSIZE	= '06'
uCamIII_CMD_SET_BAUDRATE	= '07'
uCamIII_CMD_RESET			= '08'
uCamIII_CMD_DATA			= '0A'
uCamIII_CMD_SYNC			= '0D'
uCamIII_CMD_ACK				= '0E'
uCamIII_CMD_NAK				= '0F'
uCamIII_CMD_SET_FREQ		= '13'
uCamIII_CMD_SET_CBE			= '14'
uCamIII_CMD_SLEEP			= '15'
uCamIII_DONT_CARE			= 'FF'

uCamIII_RAW_8BIT          = '03'
uCamIII_RAW_16BIT_RGB565  = '06'
uCamIII_COMP_JPEG         = '07'
uCamIII_RAW_16BIT_CRYCBY  = '08'


uCamIII_80x60             = '01'
uCamIII_160x120           = '03'
uCamIII_160x128           = '03'
uCamIII_320x240           = '05'
uCamIII_640x480           = '07'
uCamIII_128x96            = '08'
uCamIII_128x128           = '09'


uCamIII_TYPE_SNAPSHOT     = '01'
uCamIII_TYPE_RAW          = '02'
uCamIII_TYPE_JPEG         = '05'


uCamIII_SNAP_JPEG         = '00'
uCamIII_SNAP_RAW          = '01'

uCamIII_RESET_FULL        = '00'
uCamIII_RESET_STATE       = '01'
uCamIII_RESET_FORCE       = 'FF'

uCamIII_50Hz              = '00'
uCamIII_60Hz              = '01'

uCamIII_MIN               = '00'  # Exposure -2
uCamIII_LOW               = '01'  #          -1
uCamIII_DEFAULT           = '02'  #           0
uCamIII_HIGH              = '03'  #          +1
uCamIII_MAX               = '04'  #          +2


uCamIII_ERROR_PIC_TYPE    = '01'
uCamIII_ERROR_PIC_UPSCALE = '02'  
uCamIII_ERROR_PIC_SCALE   = '03'  
uCamIII_ERROR_UNEXP_REPLY = '04'  
uCamIII_ERROR_PIC_TIMEOUT = '05'  
uCamIII_ERROR_UNEXP_CMD   = '06'  
uCamIII_ERROR_JPEG_TYPE   = '07'  
uCamIII_ERROR_JPEG_SIZE   = '08'  
uCamIII_ERROR_PIC_FORMAT  = '09'  
uCamIII_ERROR_PIC_SIZE    = '0A'  
uCamIII_ERROR_PARAM       = '0B'  
uCamIII_ERROR_SEND_TIMEOUT= '0C'  
uCamIII_ERROR_CMD_ID      = '0D'  
uCamIII_ERROR_PIC_NOT_RDY = '0F'  
uCamIII_ERROR_PKG_NUM     = '10'  
uCamIII_ERROR_PKG_SIZE    = '11'
uCamIII_ERROR_CMD_HEADER  = 'F0'
uCamIII_ERROR_CMD_LENGTH  = 'F1'   
uCamIII_ERROR_PIC_SEND    = 'F5'   
uCamIII_ERROR_CMD_SEND    = 'FF'  


def comb_cmd(cmd_id, param1, param2, param3, param4):
    return ''.join([ID, cmd_id, param1, param2, param3, param4])

def init_cmd(picCmd, rawRes_cmd, jpegRes_cmd):
    return comb_cmd(uCamIII_CMD_INIT, '00', picCmd, rawRes_cmd, jpegRes_cmd)

def get_pic(picType):
    return comb_cmd(uCamIII_CMD_GET_PICTURE, picType, '00', '00', '00')

def snapshot(snapType, lowByte, highByte):
    return comb_cmd(uCamIII_CMD_SNAPSHOT, snapType, lowByte, highByte, '00')

def set_pkg_size(highByte, lowByte):
    return comb_cmd(uCamIII_CMD_SET_PACKSIZE, '08', lowByte, highByte, '00')

def set_baud_rate():
    return comb_cmd(uCamIII_CMD_SET_BAUDRATE, 'div1', 'div2', '00', '00')

def reset():
    return comb_cmd(uCamIII_CMD_RESET, 'type', '00', '00', 'FF')

def sync():
    return comb_cmd(uCamIII_CMD_SYNC, '00', '00', '00', '00')

def ack_cmd(cmd_id, ack_counter, id1='00', id2='00'):
    return comb_cmd(uCamIII_CMD_ACK, cmd_id, ack_counter, id1, id2)

def data(dataType, len1, len2, len3):
    return comb_cmd(uCamIII_CMD_DATA, dataType, len1, len2, len3)
