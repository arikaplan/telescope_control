# move from some initial position to a final position

import planets
import config
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib
'''
def wait(c):
    while int(float(c('MG _BGA'))) == 1 or int(float(c('MG _BGB'))) == 1:
        pass
'''
def wait(c):
    while c('MG _BGA') != '0.0000' or c('MG _BGB') != '0.0000':
        #print(c('MG _BGA'),c('MG _BGB'))
        pass

def location(az, el, c):
  #g = gclib.py() #make an instance of the gclib python class
  
  try:
    

    #print('gclib version:', g.GVersion())
    #g.GOpen('COM1 --direct')
    #print(g.GInfo())

    c = c

    ######################################

    # deg to ct conversion for each motor
    degtoctsAZ = config.degtoctsAZ
    degtoctsE = config.degtoctsE

    #where you are currently
    P1AZ = float(c('TPX')) % 1024000
    P1E = float(c('TPY')) % 4096
    print('AZ_0:', P1AZ / degtoctsAZ, 'Elev_0:', P1E / degtoctsE)

    #az el you want to go to
    AZ = az
    E = el

    #keep telescope from pointing below horizon
    if E < 0. or E > 180.:
        print('Warning, this elevation is below the horizon, your going to break the telescope...')
        return 

    #convert new coordinates to cts
    P2AZ = AZ % 360 * degtoctsAZ
    P2E = E % 360 * degtoctsE
    
    #azimuth scan settings
    azSP = config.azSP # 90 deg/sec
    azAC = config.azAC # acceleration 
    azDC = config.azDC # deceleration

    azD = (P2AZ - P1AZ) # distance to desired az
    
    #make it rotate the short way round
    if azD > 180. * degtoctsAZ:
        azD = azD - 360.*degtoctsAZ

    if azD < -180. * degtoctsAZ:
        azD = 360. * degtoctsAZ + azD

    #print(azD / degtoctsAZ, '!!!!!!!!!!!!!!!!!!!!!!')
    
    #elevation settings
    elevSP = config.elevSP # x degrees/sec
    elevAC = config.elevAC # acceleration 
    elevDC = config.elevDC # deceleration

    elevD = (P2E - P1E) # distance to desired elev
    
    #make it rotate the short way round, this might be unecessary for el
    if elevD > 180. * degtoctsE:
        elevD = elevD - 360. * degtoctsE
    
    if elevD < -180. * degtoctsE:
        elevD = 360. * degtoctsE + elevD

    #gclib/galil commands to move az motor
    c('SPA=' + str(azSP)) #speed, cts/sec
    c('ACA=' + str(azAC)) #speed, cts/sec
    c('DCA=' + str(azDC)) #speed, cts/sec
    c('PRA=' + str(azD)) #relative move

    #gclib/galil commands to move elevation motor
    c('SPB=' + str(elevSP)) #elevation speed
    c('ACB=' + str(elevAC)) #speed, cts/sec
    c('DCB=' + str(elevDC)) #speed, cts/sec
    c('PRB=' + str(elevD)) #relative move

    print('Moving to object location')
    c('BGA') #begin motion 
    #g.GMotionComplete('A')
    wait(c)
    if c('MG _SCA') != '1.0000':
        return

    c('BGB') # begin motion

    #wait for both az and el motors to finish moving
    #c('AMB')
    #c('AMA')
    wait(c)

    #if it hasnt reached its intended position, 
    #its because I stopped it and the function should end
    if c('MG _SCB') != '1.0000':
        return
    #g.GMotionComplete('A')
    #g.GMotionComplete('B')
    print(' done.')

    print('AZ_f:', P2AZ/degtoctsAZ, 'Elev_f:', P2E/degtoctsE)
 
    del c #delete the alias

  ###########################################################################
  # except handler
  ###########################################################################  
  except gclib.GclibError as e:
    print('Unexpected GclibError:', e)
  
  return

def distance(az, el, c):
  #g = gclib.py() #make an instance of the gclib python class
  
  try:
    print('Moving now...')

    #print('gclib version:', g.GVersion())
    #g.GOpen('COM1 --direct')
    #print(g.GInfo())

    c = c

    ######################################

    # deg to ct conversion for each motor
    degtoctsAZ = config.degtoctsAZ
    degtoctsE = config.degtoctsE

    #where you are currently
    print(c('TPX'))
    P1AZ = float(c('TPX'))
    P1E = float(c('TPY'))
    print('AZ_0:', P1AZ % 1024000 / degtoctsAZ, 'Elev_0:', P1E % 4096 / degtoctsE)

    #az el you want to move by
    AZ = az
    E = el

    #keep telescope from pointing below horizon
    if E < 0. or E > 180.:
        print('Warning, this elevation is below the horizon, your going to break the telescope...')
        return 

    #convert new coordinates to cts
    P2AZ = AZ  * degtoctsAZ
    P2E = E  * degtoctsE
    
    #azimuth scan settings
    azSP = config.azSP # 90 deg/sec
    azAC = config.azAC # acceleration 
    azDC = config.azDC # deceleration

    azD = P2AZ # distance to desired az
    
    #elevation settings
    elevSP = config.elevSP # x degrees/sec
    elevAC = config.elevAC # acceleration 
    elevDC = config.elevDC # deceleration

    elevD = P2E # distance to move elev by

    #gclib/galil commands to move az motor
    c('SPA=' + str(azSP)) #speed, cts/sec
    c('ACA=' + str(azAC)) #speed, cts/sec
    c('DCA=' + str(azDC)) #speed, cts/sec
    c('PRA=' + str(azD)) #relative move

    #gclib/galil commands to move elevation motor
    c('SPB=' + str(elevSP)) #elevation speed
    c('ACB=' + str(elevAC)) #speed, cts/sec
    c('DCB=' + str(elevDC)) #speed, cts/sec
    c('PRB=' + str(elevD)) #relative move

    print(' Starting Motion...')

    c('BGA') #begin motion 
    #g.GMotionComplete('A')
    wait(c)

    #if it hasnt reached its intended position, 
    #its because I stopped it and the function should end
    if c('MG _SCA') != '1.0000':
        return

    c('BGB') # begin motion

    #wait for both az and el motors to finish moving
    wait(c)

    #if it hasnt reached its intended position, 
    #its because I stopped it and the function should end
    if c('MG _SCB') != '1.0000':
        return
    #c('AMA')
    #c('AMB')
    #g.GMotionComplete('A')
    #g.GMotionComplete('B')
    print(' done.')

    print('AZ_f:', (P1AZ + P2AZ)/degtoctsAZ % 360, 'Elev_f:', (P1E + P2E)/degtoctsE % 360)
 
    del c #delete the alias

  ###########################################################################
  # except handler
  ###########################################################################  
  except gclib.GclibError as e:
    print('Unexpected GclibError:', e)
  
  return
  
'''
g = gclib.py()
g.GOpen('10.1.2.245 --direct -s ALL')
c = g.GCommand

az = 90
el = 0

#location(az, el, c)
distance(az, el, c)
'''