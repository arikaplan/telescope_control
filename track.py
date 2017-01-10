import moveto
import planets
import scan
import gclib

g = gclib.py()
g.GOpen('10.1.2.245 --direct -s ALL')
c = g.GCommand

c('AB') #abort motion and program
c('MO') #turn off all motors
c('SH') #servo on


location = "UCSB"
cbody = "Sun"
#az, el = planets.getlocation(location, cbody)

#linear scan
#+/- azimuth you want to go to
MinAz = -10
MaxAz = 10

MinEl = -10
MaxEl = 10

stepSize = 10.

numAzScans = 2


#az, el = planets.getlocation(location, cbody)
#moveto.location(az, el)
#scan.linearScan(location, cbody, numAzScans, MinAz, MaxAz, c)

scan.horizontalScan(location, cbody, numAzScans, MinAz, MaxAz, MinEl, MaxEl, stepSize, c)




g.GClose() #don't forget to close connections!



#now set it up to go scan back and forth around object