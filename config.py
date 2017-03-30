#control paramters

# deg to ct conversion for each motor
global degtoctsAZ 
degtoctsAZ = 1024000./360.
global degtoctsE 
degtoctsE = 4096./360.
    
#azimuth scan settings
global azSP 
azSP = 10 * degtoctsAZ # az scan speed, 90 deg/sec
global azAC
azAC = 180 * degtoctsAZ # acceleration 
global azDC
azDC = azAC # deceleration

#elevation settings
global elevSP
elevSP = 180 * degtoctsE # x degrees/sec
global elevAC
elevAC = 360 * degtoctsAZ # acceleration 
global elevDC
elevDC = elevAC # deceleration

#azimuth move settings
global azSPm 
azSPm = 90 * degtoctsAZ # az scan speed, 90 deg/sec

