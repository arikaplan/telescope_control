import scan
import moveto
import config
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
sys.path.append('data_aquisition')
import converter
import gclib
import threading
import time
import numpy as np
#from tkinter import ttk #this is for python 3
#from tkinter import *   #this is for python 3
from Tkinter import *    #this is for python 2.7
import ttk               #this is for python 2.7

#make an instance of the gclib python class
g = gclib.py()
#connect to network
g.GOpen('10.1.2.245 --direct -s ALL')
#g.GOpen('10.1.2.250 --direct -s ALL')
#g.GOpen('COM1 --direct')
#used for galil commands
c = g.GCommand

#make it again for the output frame
g2 = gclib.py()
#connect to network
g2.GOpen('10.1.2.245 --direct -s ALL')
#g2.GOpen('10.1.2.250 --direct -s ALL')
#g.GOpen('COM1 --direct')
#used for galil commands
c2 = g2.GCommand

c('AB') #abort motion and program
c('MO') #turn off all motors
c('SH') #servo on
#c('KD 2')

degtoctsAZ = config.degtoctsAZ
degtoctsE = config.degtoctsE

azgain = config.azgain
elgain = config.elgain
eloffset = config.eloffset
azoffset = config.azoffset

class interface:

    def __init__(self, master):#, interval = 0.2): 

        mainFrame = Frame(master)
        mainFrame.pack()

        nb = ttk.Notebook(mainFrame)

        outputframe = Frame(mainFrame)
        outputframe.pack(side=RIGHT)

        ##### azimuth scan #####
        page1 = Frame(nb)

        #topframe = Frame(page1)
        #topframe.pack(side=TOP)

        inputframe = Frame(page1)
        inputframe.pack(side=TOP)

        buttonframe = Frame(page1)
        buttonframe.pack(side=BOTTOM)

        #self.title = Label(topframe, text = 'Az Scan')
        #self.title.pack()

        self.l1 = Label(inputframe, text='Scan Time (seconds)')
        self.l1.grid(row = 0, column = 0, sticky=W)
        self.l2 = Label(inputframe, text='Iteration #')
        self.l2.grid(row = 1, column = 0, sticky=W)
        self.l3 = Label(inputframe, text='El Step Size (deg)')
        self.l3.grid(row = 2, column = 0, sticky=W)
        #self.l4 = Label(inputframe, text='Starting AZ (deg)')
        #self.l4.grid(row = 3, column = 0, sticky=W)
        #self.l5 = Label(inputframe, text='Starting EL (deg)')
        #self.l5.grid(row = 4, column = 0, sticky=W)

        #user input
        self.tscan = Entry(inputframe)
        self.tscan.insert(END, '5.0')
        self.tscan.grid(row = 0, column = 1)

        self.iterations = Entry(inputframe)
        self.iterations.insert(END, '2')
        self.iterations.grid(row = 1, column = 1)

        self.deltaEl = Entry(inputframe)
        self.deltaEl.insert(END, '90.0')
        self.deltaEl.grid(row = 2, column = 1)

        #self.az0 = Entry(inputframe)
        #self.az0.insert(END, '0.0')
        #self.az0.grid(row = 3, column = 1)

        #self.el0 = Entry(inputframe)
        #self.el0.insert(END, '60.0')
        #self.el0.grid(row = 4, column = 1)

        self.scan = Button(buttonframe, 
            text='Start Scan', 
            command=self.scanAz)
        self.scan.pack(side=LEFT)


        ###### tracking  ######
        nb2 = ttk.Notebook(nb)

        ###### linear scan ######
        page2 = Frame(nb2)
        inputframe = Frame(page2)
        inputframe.pack(side=TOP)

        buttonframe = Frame(page2)
        buttonframe.pack(side=BOTTOM)

        self.l1 = Label(inputframe, text='Location')
        self.l1.grid(row = 0, column = 0, sticky=W)
        self.l2 = Label(inputframe, text='Celestial Object')
        self.l2.grid(row = 1, column = 0, sticky=W)
        self.l3 = Label(inputframe, text='Az Scan #')
        self.l3.grid(row = 2, column = 0, sticky=W)
        self.l4 = Label(inputframe, text='Min Az')
        self.l4.grid(row = 3, column = 0, sticky=W)
        self.l5 = Label(inputframe, text='Max AZ')
        self.l5.grid(row = 4, column = 0, sticky=W)

        #user input
        self.location_lin = Entry(inputframe)
        self.location_lin.insert(END, 'UCSB')
        self.location_lin.grid(row = 0, column = 1)

        self.cbody_lin = Entry(inputframe)
        self.cbody_lin.insert(END, 'Neptune')
        self.cbody_lin.grid(row = 1, column = 1)

        self.numAzScans_lin = Entry(inputframe)
        self.numAzScans_lin.insert(END, '2')
        self.numAzScans_lin.grid(row = 2, column = 1)

        self.MinAz_lin = Entry(inputframe)
        self.MinAz_lin.insert(END, '-10.0')
        self.MinAz_lin.grid(row = 3, column = 1)

        self.MaxAz_lin = Entry(inputframe)
        self.MaxAz_lin.insert(END, '10.0')
        self.MaxAz_lin.grid(row = 4, column = 1)

        self.scan = Button(buttonframe, 
            text='Start Scan', 
            command=self.linear)
        self.scan.pack(side=LEFT)

        ###### horizontal scan ######
        page3 = Frame(nb2)
        inputframe = Frame(page3)
        inputframe.pack(side=TOP)

        buttonframe = Frame(page3)
        buttonframe.pack(side=BOTTOM)

        self.l1 = Label(inputframe, text='Location')
        self.l1.grid(row = 0, column = 0, sticky=W)
        self.l2 = Label(inputframe, text='Celestial Object')
        self.l2.grid(row = 1, column = 0, sticky=W)
        self.l3 = Label(inputframe, text='Az Scan #')
        self.l3.grid(row = 2, column = 0, sticky=W)
        self.l4 = Label(inputframe, text='Min Az')
        self.l4.grid(row = 3, column = 0, sticky=W)
        self.l5 = Label(inputframe, text='Max AZ')
        self.l5.grid(row = 4, column = 0, sticky=W)
        self.l6 = Label(inputframe, text='Min El')
        self.l6.grid(row = 5, column = 0, sticky=W)
        self.l7 = Label(inputframe, text='Max El')
        self.l7.grid(row = 6, column = 0, sticky=W)
        self.l8 = Label(inputframe, text='Step Size')
        self.l8.grid(row = 7, column = 0, sticky=W)

        #user input
        self.location_hor = Entry(inputframe)
        self.location_hor.insert(END, 'UCSB')
        self.location_hor.grid(row = 0, column = 1)

        self.cbody_hor = Entry(inputframe)
        self.cbody_hor.insert(END, 'Neptune')
        self.cbody_hor.grid(row = 1, column = 1)

        self.numAzScans_hor = Entry(inputframe)
        self.numAzScans_hor.insert(END, '2')
        self.numAzScans_hor.grid(row = 2, column = 1)

        self.MinAz_hor = Entry(inputframe)
        self.MinAz_hor.insert(END, '-10.0')
        self.MinAz_hor.grid(row = 3, column = 1)

        self.MaxAz_hor = Entry(inputframe)
        self.MaxAz_hor.insert(END, '10.0')
        self.MaxAz_hor.grid(row = 4, column = 1)

        self.MinEl = Entry(inputframe)
        self.MinEl.insert(END, '-10.0')
        self.MinEl.grid(row = 5, column = 1)

        self.MaxEl = Entry(inputframe)
        self.MaxEl.insert(END, '10.0')
        self.MaxEl.grid(row = 6, column = 1)

        self.stepSize = Entry(inputframe)
        self.stepSize.insert(END, '10.0')
        self.stepSize.grid(row = 7, column = 1)

        self.scan = Button(buttonframe, 
            text='Start Scan', 
            command=self.horizontal)
        self.scan.pack(side=LEFT)


        ####### move distance page #########
        movePage = Frame(nb)

        moveDFrame = Frame(movePage)
        moveDFrame.pack()

        movetoFrame = Frame(movePage)
        movetoFrame.pack(side=TOP)

        labelD = Label(moveDFrame, text = 'Move Distance')
        labelD.pack()

        inputframe = Frame(moveDFrame)
        inputframe.pack(side=TOP)

        buttonframe = Frame(moveDFrame)
        buttonframe.pack(side=BOTTOM)

        self.l1 = Label(inputframe, text='az')
        self.l1.grid(row = 0, column = 0, sticky=W)

        self.l2 = Label(inputframe, text='el')
        self.l2.grid(row = 1, column = 0, sticky=W)

        #user input
        self.az = Entry(inputframe)
        self.az.insert(END, '10.0')
        self.az.grid(row = 0, column = 1)

        self.el = Entry(inputframe)
        self.el.insert(END, '0.0')
        self.el.grid(row = 1, column = 1)

        self.scan = Button(buttonframe, 
            text='Start Move', command=self.moveDist)
        self.scan.pack(side=LEFT)

        ########## move to #############

        labelto = Label(movetoFrame, text = 'Move to location')
        labelto.pack()

        inputframe2 = Frame(movetoFrame)
        inputframe2.pack(side=TOP)

        buttonframe2 = Frame(movetoFrame)
        buttonframe2.pack(side=BOTTOM)

        self.l3 = Label(inputframe2, text='az')
        self.l3.grid(row = 0, column = 0, sticky=W)

        self.l4 = Label(inputframe2, text='el')
        self.l4.grid(row = 1, column = 0, sticky=W)

        #user input
        self.az2 = Entry(inputframe2)
        self.az2.insert(END, '0.0')
        self.az2.grid(row = 0, column = 1)

        self.el2 = Entry(inputframe2)
        self.el2.insert(END, '0.0')
        self.el2.grid(row = 1, column = 1)

        self.scan = Button(buttonframe2, 
            text='Start Move', command=self.moveTo)
        self.scan.pack(side=LEFT)


        ####### notebook layout #########
        nb.add(movePage, text='Move')
        nb.add(page1, text='Az Scan')
        nb.add(nb2, text='Track')
        nb2.add(page2, text = 'Linear Scan')
        nb2.add(page3, text = 'Horizontal Scan')


        nb.pack(expand=1, fill="both")

        ####### output frame ##### 
        
        outputframe1 = Frame(outputframe)
        outputframe1.pack()

        outputframe2 = Frame(outputframe)
        outputframe2.pack()
        
        self.title = Label(outputframe1, text='Feedback')
        self.title.pack()

        self.laz = Label(outputframe2, text='az')
        self.laz.grid(row = 1, column = 0, sticky = E)

        self.aztxt = Text(outputframe2, height = 1, width = 15)
        self.aztxt.grid(row = 1, column = 1)

        self.lalt = Label(outputframe2, text='alt')
        self.lalt.grid(row = 2, column = 0, sticky = E)

        self.alttxt = Text(outputframe2, height = 1, width = 15)
        self.alttxt.grid(row = 2, column = 1)
        
        #thread stuff
        #self.interval = interval
        thread = threading.Thread(target=self.moniter, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start() 

        ############# stop frame ###############
        
        bottomFrame = Frame(mainFrame)
        bottomFrame.pack(side=BOTTOM)


        self.stopbutton = Button(mainFrame, text='Stop', command=self.stop)
        self.stopbutton.pack(side=LEFT)

        self.quitButton = Button(mainFrame, text='Exit', command=master.quit)
        self.quitButton.pack(side=LEFT)
        
    '''
    #keep this in case I want to compare encoder postion to galil position
    # i.e. moniter both at the same time
    def moniter(self):

        t1 = time.time()

        while True:
            
            t2 = time.time()
            dt = t2 - t1
            
            if dt >= 2:
                Paz = (float(c2('TPX')) % 1024000) / degtoctsAZ
                Palt = (float(c2('TPY')) % 4096) / degtoctsE
                self.aztxt.delete('1.0', END)
                self.aztxt.insert('1.0', Paz)
                self.alttxt.delete('1.0', END)
                self.alttxt.insert('1.0', Palt)
                #this is currently asking galil for position, it needs to ask encoder

                #time.sleep(self.interval) 
           
    '''
    def moniter(self):

        if len(sys.argv)==1: #this is the defualt no argument write time
            sys.argv.append(60) #this sets how long it takes to write a file
        #data = np.zeros(1000, dtype=[("first", np.int), ("second", np.int)])
        eye = converter.getData.Eyeball()
        Data = converter.datacollector()

        #converter.fileStruct(Data.getData()) 

        time_a = time.time()
        while True:
            #timer loop
            all = eye.getData()
            
            all = (converter.bcd_to_int(all[0]), converter.bin_to_int(all[1]), converter.bin_to_int(all[2]))
            
            el=eloffset+elgain*all[0]
            az=np.mod(azoffset + azgain*all[1],360.)
            rev=all[2]
            Data.add(el,az,rev)
            #print Data.getData()
            time_b = time.time()
            delta = time_b-time_a
            if (delta>=2):
                #print(rev,az,el)
                self.aztxt.delete('1.0', END)
                self.aztxt.insert('1.0', az)
                self.alttxt.delete('1.0', END)
                self.alttxt.insert('1.0', el)

            if(delta>=int(sys.argv[1])): 
                converter.fileStruct(Data.getData(), Data)
                time_a=time.time();
                print("file written")
                
        print("data collected at" + str(1.0/delta) +"HZ")

      
    def scanAz(self):

        tscan = float(self.tscan.get())
        iterations = int(self.iterations.get())
        deltaEl = float(self.deltaEl.get())

        thread = threading.Thread(target=scan.azScan, args=(tscan, iterations, deltaEl, c))
        thread.daemon = True
        thread.start()

        #scan.azScan(tscan, iterations, deltaEl, c)

    def linear(self):
        location = self.location_lin.get()
        cbody = self.cbody_lin.get()
        numAzScans = int(self.numAzScans_lin.get())
        MinAz = float(self.MinAz_lin.get())
        MaxAz = float(self.MaxAz_lin.get())

        thread = threading.Thread(target=scan.linearScan, args=(location, cbody, numAzScans, MinAz, MaxAz, c))
        thread.daemon = True
        thread.start()

        #scan.linearScan(location, cbody, numAzScans, MinAz, MaxAz, c)

    def horizontal(self):
        location = self.location_hor.get()
        cbody = self.cbody_hor.get()
        numAzScans = int(self.numAzScans_hor.get())
        MinAz = float(self.MinAz_hor.get())
        MaxAz = float(self.MaxAz_hor.get())
        MinEl = float(self.MinEl.get())
        MaxEl = float(self.MaxEl.get())
        stepSize = float(self.stepSize.get())

        thread = threading.Thread(target=scan.horizontalScan, args=(location, cbody, numAzScans, MinAz, MaxAz, MinEl, MaxEl, stepSize, c))
        thread.daemon = True
        thread.start()

        #scan.horizontalScan(location, cbody, numAzScans, MinAz, MaxAz, MinEl, MaxEl, stepSize, c)

    def moveDist(self):
        az = float(self.az.get())
        el = float(self.el.get())

        thread = threading.Thread(target=moveto.distance, args=(az, el, c))
        thread.daemon = True
        thread.start()

        #moveto.distance(az, el, c)


    def moveTo(self):
        az = float(self.az2.get())
        el = float(self.el2.get())

        thread = threading.Thread(target=moveto.location, args=(az, el, c))
        thread.daemon = True
        thread.start()

        #moveto.location(az, el, c)


    #this does not currently work
    
    def stop(self):
        print('stopping motion...')
        c('ST')
    

root = Tk()
root.title("Telescope Control")

b = interface(root)

root.mainloop()

g.GClose() #close connections