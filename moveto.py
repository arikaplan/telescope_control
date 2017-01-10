#import gclib
import planets

import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib

def location(az, el, c):
  #g = gclib.py() #make an instance of the gclib python class
  
  try:
    #print('gclib version:', g.GVersion())
    print('Moving to object location')

    ###########################################################################
    #  Connect
    ###########################################################################
    #g.GOpen('10.1.2.245 --direct -s ALL')
    #g.GOpen('10.1.2.250 --direct -s ALL')
    #g.GOpen('COM1 --direct')
    #print(g.GInfo())

    #Motion Complete

    #c = g.GCommand
    c = c

    #c('AB') #abort motion and program
    #c('MO') #turn off all motors
    #ygc('SH') #servo on

    #you should put some logic here or somewhere else that makes it always start at the same encoder position for each axis,
    #it seems like wherever it is right now when it turns on is set as the 0 position. Or just make sure it knows its current position
    #relative to some set 0
    

    ######################################
    degtoctsAZ = 1024000/360
    degtoctsE = 4096/360

    #where you are currently
    P1AZ = float(c('TPX'))
    P1E = float(c('TPY'))
    print('AZ_0:', P1AZ % 1024000 / degtoctsAZ, 'Elev_0:', P1E % 4096 / degtoctsE)

    #az el you want to go to
    AZ = az
    E = el

    #keep telescope from pointing below horizon
    if E < 0. or E > 180.:
        print('Warning, this elevation is below the horizon, your going to break the telescope...')
        return 

    #convert to cts
    P2AZ = AZ % 360 * degtoctsAZ
    P2E = E % 360 * degtoctsE
    

    #azimuth settings
    azSP = 90 * degtoctsAZ # 90 deg/sec
    azD = (P2AZ - P1AZ) # move to desired az
    
    #make it rotate the short way round
    if azD > 180. * degtoctsAZ:
        azD = azD - 360.*degtoctsAZ

    if azD < -180. * degtoctsAZ:
        azD = 360. * degtoctsAZ + azD
    
    #elevation settings
    elevSP = 180 * degtoctsE # x degrees/sec
    elevD = (P2E - P1E) # move to desired elev
    
    #make it rotate the short way round, this might be unecessary
    if elevD > 180. * degtoctsE:
        elevD = elevD - 360. * degtoctsE
    
    if elevD < -180. * degtoctsE:
        elevD = 360. * degtoctsE + elevD
    #print 'elevation!!', elevD
    

    c('SPA=' + str(azSP)) #speed, cts/sec
    c('PRA=' + str(azD)) #relative move
    print(' Starting Motion...')
    c('BGA') #begin motion
    #c('AMA')
    #g.GMotionComplete('A')
    

    c('SPB=' + str(elevSP)) #elevation speed
    c('PRB=' + str(elevD)) # change the elevation by x deg
    c('BGB')
    c('AMB')
    c('AMA')
    print(' done.')

    #count += 1

    #print(c('TP'))
    print('AZ_f:', P2AZ/degtoctsAZ, 'Elev_f:', P2E/degtoctsE)
    #############################################################

    #P2A = float(c('TPX'))
    #deltaA = (P2A - P1A) / degtoctsA
    #print 'delta A:', deltaA
    
    del c #delete the alias

  ###########################################################################
  # except handler
  ###########################################################################  
  except gclib.GclibError as e:
    print('Unexpected GclibError:', e)
  
  #finally:
  #  g.GClose() #don't forget to close connections!
  
  return
  
 
#runs main() if example.py called from the console
#if __name__ == '__location__':
#  location()
'''
g = gclib.py()
g.GOpen('10.1.2.245 --direct -s ALL')
c = g.GCommand

az = 5
el = 170

location(az, el, c)
'''