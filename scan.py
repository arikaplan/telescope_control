#script for linear and horizontal scan patterns

import moveto
import planets
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib

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
    #time = 2 # move for 2 seconds
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
    #time = 2 # move for 2 seconds
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
          c('PRA=' + str(MinCT - MaxCT)) #relative move, 1024000 cts = 360 degrees
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
  