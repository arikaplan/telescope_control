import h5py as h5
import matplotlib.pyplot as plt
import numpy as np
from plot_path import open_folder
from plot_path import select_file

'''
Plot 3 variables hdf5 data in one figure
Given path of folder (characterized by year, month, and day)
Given path of files (characterized by a starting time and an ending time)
'''
def conti_test(year,month,day,st_hour,st_minute,ed_hour,ed_minute):
    
    d_h=ed_hour-st_hour
    d_m=ed_minute-st_minute
    time_range=abs(d_h)*60+(d_m)+1
    
    open_folder(month,day,year)
    files=select_file(st_hour,st_minute,ed_hour,ed_minute)

    minute=[]
    for i in range(len(files)):
        minute.append(int(files[i][0:2])*60+int(files[i][3:5]))
        print('# of files:',len(minute))
        print('Time range:',time_range)
        
    if len(minute)!=time_range:
        print "Files are discontinuous"
        return minute
    else:
        print 'Files are continuous'        
        return minute


def plot_h5(var, year, month, day,st_hour,st_minute,ed_hour,ed_minute):
    
    open_folder(month,day,year)
    files=select_file(st_hour,st_minute,ed_hour,ed_minute)

    #m=conti_test(year,month,day,st_hour,st_minute,ed_hour,ed_minute)
    
    #size=0
    for fname in files:
        with h5.File(fname,'r') as f:
            var1 = f['data']['%s' % var]
            #el=f['data']['el']
            #az=f['data']['az']
            #rev=f['data']['rev']
            var2 = f['data']['gpstime']
        var1=np.array(var1)
        t=np.array(var2)
        var1=var1[np.logical_not(var1==0)]

        t=t[np.logical_not(t==0)]
        #size=len(var1)
        #t=np.linspace(int(m[i-1]),1+int(m[i-1]),size)
        

        #el,=plt.plot(t,el,'b',label='el')
        #az,=plt.plot(t,az,'k',label='az')
        #rev,=plt.plot(t,rev,'r--',label='rev')

        plt.plot(t, var1, 'b-', linewidth = 2)
        plt.ylabel('%s (deg)' % var)
        plt.xlabel('Time(minute)')
        #plt.legend(handles=[el,az,rev])
    plt.show()

if __name__=="__main__":
    plot_h5('el',2017,05,24,14,44,14,44)
