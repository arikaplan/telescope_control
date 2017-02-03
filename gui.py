import scan
import scantest
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib
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

	#init gets called automatically
	def __init__(self, master):


		topframe = Frame(master)
		topframe.pack()

		inputfame = Frame(master)
		inputfame.pack(side=TOP)

		buttonframe = Frame(master)
		buttonframe.pack(side=BOTTOM)

		self.title = Label(topframe, text = 'Az Scan')
		self.title.pack()

		self.l1 = Label(inputfame, text='scan time (seconds)')
		self.l1.grid(row = 0, column = 0, sticky=W)
		self.l2 = Label(inputfame, text='iteration #')
		self.l2.grid(row = 1, column = 0, sticky=W)
		self.l3 = Label(inputfame, text='El Step Size (deg)')
		self.l3.grid(row = 2, column = 0, sticky=W)
		self.l4 = Label(inputfame, text='starting az (deg)')
		self.l4.grid(row = 3, column = 0, sticky=W)
		self.l5 = Label(inputfame, text='starting el (deg)')
		self.l5.grid(row = 4, column = 0, sticky=W)

		#user input
		self.tscan = Entry(inputfame)
		self.tscan.grid(row = 0, column = 1)
		self.iterations = Entry(inputfame)
		self.iterations.grid(row = 1, column = 1)
		self.deltaEl = Entry(inputfame)
		self.deltaEl.grid(row = 2, column = 1)
		self.az0 = Entry(inputfame)
		self.az0.grid(row = 3, column = 1)
		self.el0 = Entry(inputfame)
		self.el0.grid(row = 4, column = 1)


		self.scan = Button(buttonframe, 
			text='Start Scan', 
			command=self.scanAz)
		self.scan.pack(side=LEFT)

		self.quitButton = Button(buttonframe, text='quit', command=master.quit)
		self.quitButton.pack(side=LEFT)


	def scanAz(self):

		tscan = float(self.tscan.get())
		iterations = int(self.iterations.get())
		deltaEl = float(self.deltaEl.get())
		az0 = float(self.az0.get())
		el0 = float(self.el0.get())

		scan.azScan(tscan, iterations, az0, el0, deltaEl, c)

		g.GClose() #close connections


root = Tk()

b = interface(root)

root.mainloop()

