# Tuning helper for the yaesu ft-dx10 - by DB8TS, 2022-12
# this script sets mode to cw-l, power to 5W and keys the
# transmitter for a given period of time. After transmitting
# previous mode and power settings are restored. 

import serial       # (python -m pip install pyserial)
import keyboard     # (python -m pip install keyboard)
import time
import sys

if (len(sys.argv)>1):
    timer = int(sys.argv[1])
    if (timer>=0) and (timer<=30):    

        with serial.Serial() as ser:
            ser.baudrate = 38400    # baudrate, depends on your setup
            ser.port = 'COM4'       # port, depends on your setup
            
            ser.open()
            
            ser.write(b'MD0;')      # get current mode
            mode_op = ser.read_until(b';')
            
            ser.write(b'PC;')       # get current power-setting
            power_op = ser.read_until(b';')
            
            ser.write(b'PC005;')    # set power to 5W 
            ser.write(b'MD03;')     # set mode to cw-l
            ser.write(b'TX1;')      # switch to tx
            
            if timer == 0:
                print ("\nTuning, press ESC to stop!\n")
                while True:
                    if keyboard.is_pressed("esc"):
                        break
            else:
                time.sleep(timer)               
            
            ser.write(b'RM6;')              # read swr
            buffer = ser.read_until(b';')
            swr = (buffer[3:6])
            swr = int(swr.decode("utf-8"))
            
            ser.write(b'TX0;')      #switch to rx
            time.sleep(0.1)
            ser.write(mode_op)      #set mode to previous mode
            time.sleep(0.1)
            ser.write(power_op)     #set power to previous power
            ser.close()  
            
            if (swr == 0): print ("SWR = 1")
            elif (swr <= 64): print ("SWR <= 1.5")
            elif (swr <= 96): print ("SWR <= 2")
            elif (swr <= 128): print ("SWR <= 3")
            elif (swr > 128): print ("SWR > 3 !!")
            
    else:
        print ("\n\n")
        print ("Tuning helper for the yaesu ft-dx10 - by DB8TS, 2022-12")
        print ("Syntax: " + sys.argv[0] + " + Time in seconds (between 0 and 30, 0 = tuning until ESC is pressed)")
else:
    print ("tuning helper for the yaesu ft-dx10 - by DB8TS, 2022-12")
    print ("Syntax: " + sys.argv[0] + " + Time in seconds (between 0 and 30, 0 = tuning until ESC is pressed)")
 
