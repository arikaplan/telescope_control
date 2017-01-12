#script for linear and horizontal scan patterns

import moveto
import planets
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib
from datetime import datetime, timedelta

def linearScan(location, cbody, numAzScans, MinAz, MaxAz, c):
  
  try:
    #print('gclib version:', g.GVersion())
    #g.GOpen('COM1 --direct')
    #print(g.GInfo())

    c = c

    # deg to ct conversion for each motor
    degtoctsAZ = 1024000./360.
    degtoctsE = 4096./360.
    
    #azimuth scan settings
    azSP = 90 * degtoctsAZ # az scan speed, 90 deg/sec
    MinCT = MinAz * degtoctsAZ 
    MaxCT = MaxAz * degtoctsAZ

    #loop through back and forth azimuth scans
    for i in range(0, numAzScans):

      #find az, el of varios sky objects
      az, el = planets.getlocation(location, cbody)

      print('%s az, el: ' % cbody, az, el)

      #keep the telescope from pointing below the horizon
      if el < 0. or el > 180.:
        print('Warning, this elevation is below the horizon, your going to break the telescope...')
        return 

      #forward scan
      if (i % 2) == 0:

        moveto.location(az + MinAz, el, c)

        #gclib/galil commands to move az axis motor
        c('SPA=' + str(azSP)) #speed, cts/sec
        c('PRA=' + str(MaxCT - MinCT)) #relative move
        print(' Starting forward pass: ' + str(i + 1))
        c('BGA') #begin motion
        c('AMA') # wait for motion to complete
        #g.GMotionComplete('A') # I don't know what this does
        print(' done.')

      #backwards scan
      else:

        moveto.location(az + MaxAz, el, c)

        #gclib/galil commands to move elevation axis motor
        c('SPA=' + str(azSP)) #speed, cts/sec
        c('PRA=' + str(MinCT - MaxCT)) #relative move, 1024000 cts = 360 degrees
        print(' Starting backward pass: ' + str(i))
        c('BGA') #begin motion
        c('AMA') #wait for motion to complete
        #g.GMotionComplete('A')
        print(' done.')
      
    del c #delete the alias

  ###########################################################################
  # except handler
  ###########################################################################  
  except gclib.GclibError as e:

    print('Unexpected GclibError:', e)
  
  return

def horizontalScan(location, cbody, numAzScans, MinAz, MaxAz, MinEl, MaxEl, stepSize, c):
  
  try:
    #print('gclib version:', g.GVersion())
    #g.GOpen('COM1 --direct')
    #print(g.GInfo())

    c = c
    
    # deg to ct conversion for each motor
    degtoctsAZ = 1024000./360.
    degtoctsE = 4096./360.
    
    #azimuth scan settings
    azSP = 90 * degtoctsAZ # 90 deg/sec
    MinCT = MinAz * degtoctsAZ
    MaxCT = MaxAz * degtoctsAZ

    #number of elevations to scan at, rounds to nearest integer
    numElScans = int(round(((MaxEl - MinEl + stepSize)/stepSize)))

    #loop through back and forth az scans at different elevations
    for j in range(0, numElScans):
      print('starting horizontal scan: ', j + 1)
      for i in range(0, numAzScans):

        #find az, el of varios sky objects
        az, el = planets.getlocation(location, cbody) 
       
        print('%s az, el: ' % cbody, az, el)

        #keep the telescope from pointing below the horizon
        if el + MinEl < 0. or el + MaxEl > 180.:
          print('Warning, this elevation is below the horizon, your going to break the telescope...')
          return

        #forward scan
        if (i % 2) == 0:

          moveto.location(az + MinAz, el + MinEl + j*stepSize, c)

          #gclib/galil commands to move az axis motor
          c('SPA=' + str(azSP)) #speed, cts/sec
          c('PRA=' + str(MaxCT - MinCT)) #relative move
          print(' Starting forward pass: ', i + 1)
          c('BGA') #begin motion
          c('AMA') # wait for motion to complete
          #g.GMotionComplete('A')
          print(' done.')

        #backwards scan
        else:

          moveto.location(az + MaxAz, el + MinEl + j*stepSize, c)

          #gclib/galil commands to move elevation axis motor
          c('SPA=' + str(azSP)) #speed, cts/sec
          c('PRA=' + str(MinCT - MaxCT)) #relative move
          print(' Starting backward pass: ', i)
          c('BGA') #begin motion
          c('AMA') # wait for motion to complete
          #g.GMotionComplete('A')
          print(' done.')
        

    del c #delete the alias

  ###########################################################################
  # except handler
  ###########################################################################  
  except gclib.GclibError as e:
    print('Unexpected GclibError:', e)
   
  return

def azScan(tscan, iterations, deltaEl, c):
 
  try:

    c = c
    
    # deg to ct conversion for each motor
    degtoctsAZ = 1024000/360
    degtoctsE = 4096/360
    
    #azimuth scan settings
    azSP = 90 * degtoctsAZ # 90 deg/sec
    azAC = 20 * degtoctsAZ # acceleration 
    azDC = azAC # deceleration

    #elevation settings
    elevSP = 180 * degtoctsE # x degrees/sec
    elevAC = 40 * degtoctsAZ # acceleration 
    elevDC = elevAC # deceleration
    elevD = deltaEl * degtoctsE # move elevation x degrees each iteration

    #initial position
    P1AZ = (float(c('TPX')) % 1024000) / degtoctsAZ
    P1E = (float(c('TPY')) % 4096) / degtoctsE
    print('AZ:', P1AZ, 'Elev:', P1E)

    #while count < iterations:
    for i in range(0, iterations):

      #set start time
      st = datetime.utcnow()
      #set current time to start time
      ct = st
      #duration of azimuth scan
      dt = timedelta(0, tscan)

      print(' Starting az Scan: ' + str(i + 1))

      #scan in azimuth while current time < start time + duration
      while ct < st + dt:

        #gclib/galil commands to move elevation axis motor
        c('JGA=' + str(azSP)) #speed, cts/sec
        c('ACA=' + str(azAC)) #acceleration, cts/sec
        c('DCA=' + str(azDC)) #deceleration, cts/sec
        c('BGA') #begin motion

        #update current time
        ct = datetime.utcnow()

      c('ST') # stop when duration has passed
      c('AMA') # wait for motion to stop

      print(' done.')

      #final position after each az scan
      P2AZ = (float(c('TPX'))) % 1024000 / degtoctsAZ
      P2E = float(c('TPY')) % 4096 / degtoctsE
      print('AZ:', P2AZ, 'Elev:', P2E)

      #change elevation for next az scan
      if i < iterations - 1:
        print('changing elevation')
        c('SPB=' + str(elevSP)) #elevation speed
        c('ACB=' + str(elevAC)) #acceleration, cts/sec
        c('DCB=' + str(elevDC)) #deceleration, cts/sec
        c('PRB=' + str(elevD)) # change the elevation by x deg
        c('BGB') #begin motion
        c('AMB') #wait for motion to complete
        print('done')
        

        #position after each elevation change
        P2AZ = (float(c('TPX'))) % 1024000 / degtoctsAZ
        P2E = float(c('TPY')) % 4096 / degtoctsE
        print('AZ:', P2AZ, 'Elev:', P2E)
    
    del c #delete the alias

  ###########################################################################
  # except handler
  ###########################################################################  
  except gclib.GclibError as e:
    print('Unexpected GclibError:', e)
    
  return
  