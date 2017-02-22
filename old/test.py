import sys
sys.path.append('C:/Python27x86/lib/site-packages')
sys.path.append('../')
import gclib
from datetime import datetime, timedelta


def main():

  g = gclib.py() #make an instance of the gclib python class

  try:
    
    #connect to network
    g.GOpen('10.1.2.245 --direct -s ALL')
    #print('gclib version:', g.GVersion())
    #g.GOpen('COM1 --direct')
    #print(g.GInfo())

    #used for galil commands
    c = g.GCommand
    
    c('AB') #abort motion and program
    c('MO') #turn off all motors
    c('SH') #servo on
    
    #1024000 cts = 360 degrees on motor A
    c('SPA = 90 * 1024000 / 360') # rotate at 90 deg/s
    c('ACA = 90 * 1024000 / 360') 
    c('DCA = 90 * 1024000 / 360')
    c('PRA = 1 * 1024000') # do 2 full rotations, device times out
                           # for 1 rotation, device does not time out

    #4096 cts = 360 degrees on motor B
    c('SPB = 180 * 4096 / 360') # rotate at 180 deg/s
    c('ACB = 180 * 4096 / 360')  
    c('DCB = 180 * 4096 / 360')
    c('PRB = 1 * 4096') # do one rotation

    def wait(c, axis):
        while int(float(c('MG _BG' + axis))) == 1:
            pass
    
    P1 = float(c('TPX'))
    c('BGA')

    wait(c, 'A')
    
    P2 = float(c('TPX'))
    print(P2-P1)
    #wait(c)

    c('BGB')
     

    #g.GMotionComplete('A')
    #c('AMA')
    
    #c('BGB')
    #g.GMotionComplete('B')
    #c('AMB')


    del c #delete the alias

  ###########################################################################
  # except handler
  ###########################################################################  
  except gclib.GclibError as e:
    print('Unexpected GclibError:', e)

  finally:
    g.GClose() #don't forget to close connections!
    
    #return
  
main()
#runs main() if example.py called from the console
#if __name__ == '__main__':
#  main()
  