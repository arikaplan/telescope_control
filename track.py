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

'''
######### things to do ##########
note that the precision on these scans is not perfect, figure 
out what precision is required, i think its coming from rounding 
errors and conversion between cts and degrees.

# resolved - moveto function takes the long way round when shifting elevation

add acceleration and deceleration, decide if speed 
should be set or variable

find absolute position of encoder, right not there is no reference
point

if (MaxEl - MinEl + stepSize)/stepSize is not an even integer it could
fail

code to keep telescope from pointing below horizon may need higher limit than 0
'''

#az, el = planets.getlocation(location, cbody)
#moveto.location(az, el)
#scan.linearScan(location, cbody, numAzScans, MinAz, MaxAz, c)

scan.horizontalScan(location, cbody, numAzScans, MinAz, MaxAz, MinEl, MaxEl, stepSize, c)




g.GClose() #don't forget to close connections!



#now set it up to go scan back and forth around object