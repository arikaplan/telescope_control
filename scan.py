#logic test this, it may not be doing what you want it to


#import gclib
import moveto
import planets
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib

def linearScan(location, cbody, numAzScans, MinAz, MaxAz, c):
  #g = gclib.py() #make an instance of the gclib python class
  
  try:
    #print('gclib version:', g.GVersion())

    ###########################################################################
    #  Connect
    ###########################################################################
    #g.GOpen('10.1.2.245 --direct -s ALL')
    #g.GOpen('10.1.2.250 --direct -s ALL')
    #g.GOpen('COM1 --direct')
    #print(g.GInfo())

    #Motion Complete

    c = c
    
    #c('AB') #abort motion and program
    #c('MO') #turn off all motors
    #c('SH') #servo on
    
    # deg to ct conversion for each motor
    degtoctsAZ = 1024000./360.
    degtoctsE = 4096./360.
    
    #azimuth settings
    #time = 2 # move for 2 seconds
    azSP = 90 * degtoctsAZ # 90 deg/sec
    MinCT = MinAz * degtoctsAZ
    MaxCT = MaxAz * degtoctsAZ

    #while count < iterations:

    for i in range(0, 2*numAzScans):

      az, el = planets.getlocation(location, cbody)

      print('%s az, el: ' % cbody, az, el)

      #keep the telescope from pointing below the horizon
      if el < 0. or el > 180.:
        print('Warning, this elevation is below the horizon, your going to break the telescope...')
        return 

      #forward scan
      if (i % 2) == 0:

        moveto.location(az + MinAz, el, c)
        c('SPA=' + str(azSP)) #speed, cts/sec
        c('PRA=' + str(MaxCT - MinCT)) #relative move, 1024000 cts = 360 degrees
        print(' Starting forward pass: ' + str(i + 1))
        c('BGA') #begin motion
        c('AMA')
        #g.GMotionComplete('A')
        print(' done.')

      #backwards scan
      else:

        moveto.location(az + MaxAz, el, c)
        c('SPA=' + str(azSP)) #speed, cts/sec
        c('PRA=' + str(MinCT - MaxCT)) #relative move, 1024000 cts = 360 degrees
        print(' Starting backward pass: ' + str(i))
        c('BGA') #begin motion
        c('AMA')
        #g.GMotionComplete('A')
        print(' done.')
      
      '''
      if i < iterations - 1:
        c('SPB=' + str(elevSP)) #elevation speed
        c('PRB=' + str(elevD)) # change the elevation by x deg
        c('BGB')
        c('AMB')
      '''

    del c #delete the alias

  ###########################################################################
  # except handler
  ###########################################################################  
  except gclib.GclibError as e:

    print('Unexpected GclibError:', e)
  
  #finally:
  #  g.GClose() #don't forget to close connections!
  
  return

def horizontalScan(location, cbody, numAzScans, MinAz, MaxAz, MinEl, MaxEl, stepSize, c):
  #g = gclib.py() #make an instance of the gclib python class
  
  try:
    #print('gclib version:', g.GVersion())

    ###########################################################################
    #  Connect
    ###########################################################################
    #g.GOpen('10.1.2.245 --direct -s ALL')
    #g.GOpen('10.1.2.250 --direct -s ALL')
    #g.GOpen('COM1 --direct')
    #print(g.GInfo())

    #Motion Complete

    c = c
    
    #c('AB') #abort motion and program
    #c('MO') #turn off all motors
    #c('SH') #servo on
    
    # deg to ct conversion for each motor
    degtoctsAZ = 1024000./360.
    degtoctsE = 4096./360.
    
    #azimuth settings
    #time = 2 # move for 2 seconds
    azSP = 90 * degtoctsAZ # 90 deg/sec
    MinCT = MinAz * degtoctsAZ
    MaxCT = MaxAz * degtoctsAZ

    #number of elevations to scan at, rounds to nearest integer
    numElScans = int(round(((MaxEl - MinEl + stepSize)/stepSize))

    #while count < iterations:

    for j in range(0, numElScans):
      print('starting horizontal scan: ', j + 1)
      for i in range(0, numAzScans):

        az, el = planets.getlocation(location, cbody) 
       
        print('%s az, el: ' % cbody, az, el)

        #keep the telescope from pointing below the horizon
        if el + MinEl < 0. or el + MaxEl > 180.:
          print('Warning, this elevation is below the horizon, your going to break the telescope...')
          return

        #forward scan
        if (i % 2) == 0:

          moveto.location(az + MinAz, el + MinEl + j*stepSize, c)
          c('SPA=' + str(azSP)) #speed, cts/sec
          c('PRA=' + str(MaxCT - MinCT)) #relative move, 1024000 cts = 360 degrees
          print(' Starting forward pass: ', i + 1)
          c('BGA') #begin motion
          c('AMA')
          #g.GMotionComplete('A')
          print(' done.')

        #backwards scan
        else:

          moveto.location(az + MaxAz, el + MinEl + j*stepSize, c)
          c('SPA=' + str(azSP)) #speed, cts/sec
          c('PRA=' + str(MinCT - MaxCT)) #relative move, 1024000 cts = 360 degrees
          print(' Starting backward pass: ', i)
          c('BGA') #begin motion
          c('AMA')
          #g.GMotionComplete('A')
          print(' done.')
        

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
#if __name__ == '__scan__':
#  scan()
  