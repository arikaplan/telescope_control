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
#continuity test for missing data
def conti_test(year,month,day,st_hour,st_minute,ed_hour,ed_minute):
    
    d_h=st_hour-ed_hour
    d_m=st_hour-ed_minute
    
    open_folder(year,month,day)
    files=select_file(st_hour,st_minute,ed_hour,ed_minute)

    m=[]
    for i in range(len(files)):
        m.append(int(files[i][0:2])*60+int(files[i][3:5]))
    return m



def plot_h5(year, month, day,st_hour,st_minute,ed_hour,ed_minute):
    
    open_folder(year,month,day)
    files=select_file(st_hour,st_minute,ed_hour,ed_minute)


    m=conti_test(year,month,day,st_hour,st_minute,ed_hour,ed_minute)
    
    numb=len(files)
    #print numb
    a=[]
    b=[]
    c=[]
    size=0
    i=0
    d_h=st_hour-ed_hour
    d_m=st_hour-ed_minute
    for fname in files:
        with h5.File(fname,'r') as f:
            temp = np.array(f['data'][:,0])
            print temp.shape
            var1=temp[:,0]
            print var1#[0:100]
            size=len(var1)
            print size
            var2=f['data'][:,1]
            var3=f['data'][:,2]

        a=var1
        b=var2
        c=var3

        a=np.array(a).reshape(size,1)
        b=np.array(b).reshape(size,1)
        c=np.array(c).reshape(size,1)

        i+=1
        t=np.linspace(int(m[i-1]),1+int(m[i-1]),size)
        
        

        y1,=plt.plot(t,a,'b',label='y1')
        y2,=plt.plot(t,b,'k',label='y2')
        y3,=plt.plot(t,c,'r--',label='y3')
        
        plt.xlabel('Time(minute)')
        plt.ylim([0,500])
        plt.legend(handles=[y1,y2,y3])
    plt.show()

if __name__=="__main__":
    plot_h5(2017,04,20,15,42,15,43)
    #print conti_test(2017,04,21,01,20,11,21)
  



























'''

    vars = dict(
        el=np.array(el).reshape(size,1),
        az=np.array(az).reshape(size,1),
        rev=np.array(rev).reshape(size,1)
    )
    t=np.linspace(0.0,numb,size)

#change variable name (y1,y2,y3) to anything you want
    #y1,=plt.plot(t,el,'b',label='y1')
    #y2,=plt.plot(t,az,'k',label='y2')
    #y3,=plt.plot(t,rev,'r--',label='y3')
    plt.plot(t, vars[var], 'b-', linewidth=2)
    plt.xlabel('Time(minute)')
    plt.ylabel('%s' % var)
    #plt.legend(handles=[y1,y2,y3])
    plt.show()

if __name__=="__main__":
    plot_h5('el',2017,04,20,15,42,15,43)
'''