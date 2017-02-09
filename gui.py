import scan
import scantest
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib
from tkinter import ttk
from tkinter import *

#make an instance of the gclib python class
g = gclib.py()
#connect to network
g.GOpen('10.1.2.245 --direct -s ALL')
#g.GOpen('COM1 --direct')
#used for galil commands
c = g.GCommand

c('AB') #abort motion and program
c('MO') #turn off all motors
c('SH') #servo on

class interface:

    def __init__(self, master):    

        nb = ttk.Notebook(master)

        ##### page 1 #####
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
        self.l4 = Label(inputframe, text='Starting AZ (deg)')
        self.l4.grid(row = 3, column = 0, sticky=W)
        self.l5 = Label(inputframe, text='Starting EL (deg)')
        self.l5.grid(row = 4, column = 0, sticky=W)

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

        self.az0 = Entry(inputframe)
        self.az0.insert(END, '0.0')
        self.az0.grid(row = 3, column = 1)

        self.el0 = Entry(inputframe)
        self.el0.insert(END, '60.0')
        self.el0.grid(row = 4, column = 1)

        self.scan = Button(buttonframe, 
            text='Start Scan', 
            command=self.scanAz)
        self.scan.pack(side=LEFT)

        self.quitButton = Button(buttonframe, text='quit', command=master.quit)
        self.quitButton.pack(side=LEFT)

        #self.stopButton = Button(buttonframe, text='Stop', command=self.stop)
        #self.stopButton.pack(side=LEFT)

        ###### page 2  ######
        nb2 = ttk.Notebook(nb)

        ###### page 2, tab 1 ######
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
        self.location = Entry(inputframe)
        self.location.insert(END, 'UCSB')
        self.location.grid(row = 0, column = 1)

        self.cbody = Entry(inputframe)
        self.cbody.insert(END, 'Neptune')
        self.cbody.grid(row = 1, column = 1)

        self.numAzScans = Entry(inputframe)
        self.numAzScans.insert(END, '2')
        self.numAzScans.grid(row = 2, column = 1)

        self.MinAz = Entry(inputframe)
        self.MinAz.insert(END, '-10.0')
        self.MinAz.grid(row = 3, column = 1)

        self.MaxAz = Entry(inputframe)
        self.MaxAz.insert(END, '10.0')
        self.MaxAz.grid(row = 4, column = 1)

        self.scan = Button(buttonframe, 
            text='Start Scan', 
            command=self.linear)
        self.scan.pack(side=LEFT)

        self.quitButton = Button(buttonframe, text='quit', command=master.quit)
        self.quitButton.pack(side=LEFT)

        ###### page 2, tab 2 ######
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
        self.location = Entry(inputframe)
        self.location.insert(END, 'UCSB')
        self.location.grid(row = 0, column = 1)

        self.cbody = Entry(inputframe)
        self.cbody.insert(END, 'Neptune')
        self.cbody.grid(row = 1, column = 1)

        self.numAzScans = Entry(inputframe)
        self.numAzScans.insert(END, '2')
        self.numAzScans.grid(row = 2, column = 1)

        self.MinAz = Entry(inputframe)
        self.MinAz.insert(END, '-10.0')
        self.MinAz.grid(row = 3, column = 1)

        self.MaxAz = Entry(inputframe)
        self.MaxAz.insert(END, '10.0')
        self.MaxAz.grid(row = 4, column = 1)

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

        self.quitButton = Button(buttonframe, text='quit', command=master.quit)
        self.quitButton.pack(side=LEFT)

        nb.add(page1, text='Az Scan')
        nb.add(nb2, text='Track')
        nb2.add(page2, text = 'Linear Scan')
        nb2.add(page3, text = 'Horizontal Scan')

        nb.pack(expand=1, fill="both")

    def scanAz(self):

        tscan = float(self.tscan.get())
        iterations = int(self.iterations.get())
        deltaEl = float(self.deltaEl.get())
        az0 = float(self.az0.get())
        el0 = float(self.el0.get())

        scan.azScan(tscan, iterations, az0, el0, deltaEl, c)

    def linear(self):
        location = self.location.get()
        cbody = self.cbody.get()
        numAzScans = int(self.numAzScans.get())
        MinAz = float(self.MinAz.get())
        MaxAz = float(self.MaxAz.get())

        scan.linearScan(location, cbody, numAzScans, MinAz, MaxAz, c)

    def horizontal(self):
        location = self.location.get()
        cbody = self.cbody.get()
        numAzScans = int(self.numAzScans.get())
        MinAz = float(self.MinAz.get())
        MaxAz = float(self.MaxAz.get())
        MinEl = float(self.MinEl.get())
        MaxEl = float(self.MaxEl.get())
        stepSize = float(self.stepSize.get())

        scan.horizontalScan(location, cbody, numAzScans, MinAz, MaxAz, MinEl, MaxEl, stepSize, c)

    #this does not currently work
    '''
    def stop(self):

        c('ST')
    '''

root = Tk()
root.title("Telescope Control")

b = interface(root)

root.mainloop()

g.GClose() #close connections